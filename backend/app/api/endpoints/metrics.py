# backend/app/api/endpoints/metrics.py
from fastapi import APIRouter, Depends, HTTPException
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.services.metrics_calculator import (
    calculate_pic,
    calculate_dpi,
    calculate_irr,
    get_metrics_breakdown,
)
from app.models.transaction import CapitalCall, Distribution, Adjustment

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/funds/{fund_id}/metrics")
def get_metrics(fund_id: int):
    try:
        metrics = get_metrics_breakdown(fund_id)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/funds/{fund_id}/transactions/all")
def get_all_transactions(fund_id: int, db: Session = Depends(get_db)):
    try:
        capital_calls = [
            {
                "id": c.id,
                "date": c.call_date,
                "type": f"Capital Call: {c.call_type}",
                "amount": float(c.amount),
                "description": c.description,
                "source": "capital_call",
            }
            for c in db.query(CapitalCall).filter(CapitalCall.fund_id == fund_id).all()
        ]

        distributions = [
            {
                "id": d.id,
                "date": d.distribution_date,
                "type": f"Distribution: {d.distribution_type}",
                "amount": float(d.amount),
                "description": d.description,
                "source": "distribution",
            }
            for d in db.query(Distribution).filter(Distribution.fund_id == fund_id).all()
        ]

        adjustments = [
            {
                "id": a.id,
                "date": a.adjustment_date,
                "type": f"Adjustment: {a.adjustment_type}",
                "amount": float(a.amount),
                "description": a.description,
                "source": "adjustment",
            }
            for a in db.query(Adjustment).filter(Adjustment.fund_id == fund_id).all()
        ]

        all_transactions = capital_calls + distributions + adjustments
        all_transactions.sort(key=lambda x: x["date"], reverse=True)

        return {"transactions": all_transactions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
