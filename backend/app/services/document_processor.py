import os
import pdfplumber
from datetime import datetime
from app.db.session import SessionLocal
from app.models.document import Document
from app.models.transaction import CapitalCall, Distribution, Adjustment
from app.services.embeddings import generate_embeddings
from app.services.vector_store import VectorStore
from app.services.table_parser import parse_financial_tables

UPLOAD_DIR = "/app/uploads"


def parse_document_async(document_id: int):
    """
    Extract text from a PDF, detect financial tables, store them in DB,
    then embed text chunks into FAISS vector store.
    """
    db = SessionLocal()
    doc = None
    try:
        doc = db.get(Document, document_id)
        if not doc:
            print(f"[ERROR] Document id {document_id} not found")
            return False

        file_path = doc.file_path
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(file_path or "None")

        # === Extract full text using pdfplumber ===
        full_text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text_parts.append(text)
        full_text = "\n".join(full_text_parts)

        # === [NEW] Parse tables from the extracted text ===
        parsed_data = parse_financial_tables(full_text)

        # === [NEW] Store parsed results into corresponding tables ===
        if doc.fund_id:
            if parsed_data.get("capital_calls"):
                for item in parsed_data["capital_calls"]:
                    db.add(CapitalCall(
                        fund_id=doc.fund_id,
                        call_date=datetime.strptime(item["call_date"], "%Y-%m-%d").date(),
                        call_type=item.get("call_type"),
                        amount=item["amount"],
                        description=item.get("description")
                    ))
            if parsed_data.get("distributions"):
                for item in parsed_data["distributions"]:
                    db.add(Distribution(
                        fund_id=doc.fund_id,
                        distribution_date=datetime.strptime(item["distribution_date"], "%Y-%m-%d").date(),
                        distribution_type=item.get("distribution_type"),
                        is_recallable=item.get("is_recallable", False),
                        amount=item["amount"],
                        description=item.get("description")
                    ))
            if parsed_data.get("adjustments"):
                for item in parsed_data["adjustments"]:
                    db.add(Adjustment(
                        fund_id=doc.fund_id,
                        adjustment_date=datetime.strptime(item["adjustment_date"], "%Y-%m-%d").date(),
                        adjustment_type=item.get("adjustment_type"),
                        category=item.get("category"),
                        amount=item["amount"],
                        is_contribution_adjustment=item.get("is_contribution_adjustment", False),
                        description=item.get("description")
                    ))
            db.commit()

        # === Split text into chunks ===
        chunks = chunk_text(full_text)
        if not chunks:
            raise ValueError("No text extracted from PDF")

        # === Generate embeddings ===
        embeddings = generate_embeddings(chunks)

        # === Store in FAISS vector DB (persist by fund_id) ===
        vs = VectorStore(index_name=f"fund_{doc.fund_id or 'global'}")
        vs.add_texts(chunks, embeddings)

        # === Mark parsing done ===
        doc.parsing_status = "completed"
        db.add(doc)
        db.commit()

        return True

    except Exception as e:
        if doc:
            doc.parsing_status = "error"
            doc.error_message = str(e)
            db.add(doc)
            db.commit()
        print(f"[ERROR] Document parsing failed for id {document_id}: {e}")
        return False

    finally:
        db.close()


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100):
    """
    Basic text splitter with overlap.
    """
    if not text:
        return []
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(L, start + chunk_size)
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
