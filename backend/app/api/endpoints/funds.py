from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.transaction import CapitalCall, Distribution, Adjustment
from decimal import Decimal
from app.models.fund import Fund
from app.schemas.fund import FundCreate, FundOut
import os
import glob

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/funds", response_model=list[FundOut])
def list_funds(db: Session = Depends(get_db)):
    return db.query(Fund).all()

@router.post("/funds", response_model=FundOut)
def create_fund(payload: FundCreate, db: Session = Depends(get_db)):
    f = Fund(
        name=payload.name,
        gp_name=payload.gp_name,
        fund_type=payload.fund_type,
        vintage_year=payload.vintage_year
    )
    db.add(f)
    db.commit()
    db.refresh(f)
    return f

@router.get("/funds/{fund_id}", response_model=FundOut)
def get_fund(fund_id: int, db: Session = Depends(get_db)):
    f = db.get(Fund, fund_id)
    if not f:
        raise HTTPException(status_code=404, detail="Fund not found")
    return f

@router.get("/funds/{fund_id}/transactions")
def get_fund_transactions(
    fund_id: int,
    transaction_type: str | None = Query(None, description="capital_calls | distributions | adjustments"),
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    if transaction_type is None or transaction_type == "capital_calls":
        q = db.query(CapitalCall).filter(CapitalCall.fund_id == fund_id)
    elif transaction_type == "distributions":
        q = db.query(Distribution).filter(Distribution.fund_id == fund_id)
    elif transaction_type == "adjustments":
        q = db.query(Adjustment).filter(Adjustment.fund_id == fund_id)
    else:
        raise HTTPException(status_code=400, detail="transaction_type must be one of capital_calls|distributions|adjustments")

    total = q.count()
    items = q.offset((page - 1) * limit).limit(limit).all()

    def row_to_dict(r):
        return {c.name: getattr(r, c.name) for c in r.__table__.columns}

    return {"items": [row_to_dict(i) for i in items], "total": total, "page": page, "pages": (total + limit - 1) // limit}

@router.delete("/funds/{fund_id}")
def delete_fund(fund_id: int, db: Session = Depends(get_db)):
    fund = db.get(Fund, fund_id)
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")

    db.query(CapitalCall).filter(CapitalCall.fund_id == fund_id).delete()
    db.query(Distribution).filter(Distribution.fund_id == fund_id).delete()
    db.query(Adjustment).filter(Adjustment.fund_id == fund_id).delete()

    from app.models.document import Document
    documents = db.query(Document).filter(Document.fund_id == fund_id).all()
    for doc in documents:
        try:
            if doc.file_path and os.path.exists(doc.file_path):
                os.remove(doc.file_path)
        except Exception:
            pass
        db.delete(doc)

    db.commit()

    vector_pattern = f"app/vector/fund_{fund_id}_*"
    for filepath in glob.glob(f"{vector_pattern}.pkl") + glob.glob(f"{vector_pattern}.faiss"):
        try:
            os.remove(filepath)
        except Exception:
            pass

    db.delete(fund)
    db.commit()

    return {"message": f"Fund {fund.name} dan has been deleted."}