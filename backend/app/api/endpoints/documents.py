# backend/app/api/endpoints/documents.py
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Query, BackgroundTasks
import shutil, os
from app.db.session import SessionLocal
from app.models.document import Document
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.document import DocumentOut, DocumentStatusOut

router = APIRouter()

UPLOAD_DIR = "/app/uploads" 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/documents/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    fund_id: int | None = Form(None),
    db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, f"{int(__import__('time').time())}_{file.filename}")

    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {e}")

    doc = Document(
        fund_id=fund_id,
        file_name=file.filename,
        file_path=file_path,
        parsing_status="pending"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    try:
        from app.services.document_processor import parse_document_async
        background_tasks.add_task(parse_document_async, doc.id)
    except Exception as e:
        doc.parsing_status = "error"
        doc.error_message = f"Failed to schedule parsing: {e}"
        db.add(doc)
        db.commit()
        return {
            "document_id": doc.id,
            "status": doc.parsing_status,
            "message": "Uploaded but parsing scheduling failed."
        }

    return {
        "document_id": doc.id,
        "status": doc.parsing_status,
        "message": "Uploaded. Parsing scheduled."
    }

@router.get("/documents/{document_id}", response_model=DocumentOut)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.get("/documents/{document_id}/status", response_model=DocumentStatusOut)
def get_document_status(document_id: int, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"document_id": doc.id, "status": doc.parsing_status, "error_message": doc.error_message}


@router.get("/documents", response_model=List[DocumentOut])
def list_documents(fund_id: Optional[int] = Query(None), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    q = db.query(Document)
    if fund_id is not None:
        q = q.filter(Document.fund_id == fund_id)
    items = q.offset(skip).limit(limit).all()
    return items


@router.delete("/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # delete file on disk (best-effort)
    try:
        if doc.file_path and os.path.exists(doc.file_path):
            os.remove(doc.file_path)
    except Exception:
        pass

    db.delete(doc)
    db.commit()
    return {"message": "Document deleted successfully"}
