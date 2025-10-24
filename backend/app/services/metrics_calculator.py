# backend/app/services/metrics_calculator.py
from decimal import Decimal
from sqlalchemy import func
from datetime import datetime
import numpy as np
import numpy_financial as npf

from app.db.session import SessionLocal
from app.models.transaction import CapitalCall, Distribution, Adjustment


def calculate_pic(fund_id: int) -> Decimal:
    """Paid-In Capital = Total Calls - Adjustments"""
    db = SessionLocal()
    try:
        total_calls = db.query(func.sum(CapitalCall.amount)).filter(
            CapitalCall.fund_id == fund_id
        ).scalar() or Decimal(0)

        total_adjustments = db.query(func.sum(Adjustment.amount)).filter(
            Adjustment.fund_id == fund_id
        ).scalar() or Decimal(0)

        pic = total_calls - total_adjustments
        return pic if pic > 0 else Decimal(0)
    finally:
        db.close()


def calculate_dpi(fund_id: int) -> float:
    """DPI = Total Distributions / Paid-In Capital"""
    db = SessionLocal()
    try:
        pic = calculate_pic(fund_id)

        total_distributions = db.query(func.sum(Distribution.amount)).filter(
            Distribution.fund_id == fund_id
        ).scalar() or Decimal(0)

        if not pic or pic == 0:
            return 0.0

        dpi = float(total_distributions) / float(pic)
        return round(dpi, 4)
    finally:
        db.close()


def calculate_irr(fund_id: int) -> float:
    """
    IRR = rate where NPV of all cashflows = 0
    Convention:
      - Capital Calls = negative cashflow (outflow)
      - Distributions = positive cashflow (inflow)
      - Adjustments = modify the related amount
    """
    db = SessionLocal()
    try:
        cashflows = []

        # Capital Calls (outflow)
        calls = db.query(CapitalCall.call_date, CapitalCall.amount).filter(
            CapitalCall.fund_id == fund_id
        ).all()
        for c in calls:
            cashflows.append((c.call_date, -float(c.amount)))

        # Distributions (inflow)
        dists = db.query(Distribution.distribution_date, Distribution.amount).filter(
            Distribution.fund_id == fund_id
        ).all()
        for d in dists:
            cashflows.append((d.distribution_date, float(d.amount)))

        # Adjustments
        adjs = db.query(Adjustment.adjustment_date, Adjustment.amount).filter(
            Adjustment.fund_id == fund_id
        ).all()
        for a in adjs:
            cashflows.append((a.adjustment_date, float(a.amount)))

        if not cashflows:
            return 0.0

        # Sort cashflows by date
        cashflows.sort(key=lambda x: x[0])
        values = [v for _, v in cashflows]

        irr_value = npf.irr(values)
        if irr_value is None or np.isnan(irr_value):
            return 0.0

        return round(float(irr_value), 4)
    finally:
        db.close()


def get_metrics_breakdown(fund_id: int) -> dict:
    """Show all transactions and computed metrics"""
    db = SessionLocal()
    try:
        calls = db.query(CapitalCall).filter(CapitalCall.fund_id == fund_id).all()
        dists = db.query(Distribution).filter(Distribution.fund_id == fund_id).all()
        adjs = db.query(Adjustment).filter(Adjustment.fund_id == fund_id).all()

        pic = calculate_pic(fund_id)
        dpi = calculate_dpi(fund_id)
        irr = calculate_irr(fund_id)

        return {
            "fund_id": fund_id,
            "capital_calls": [
                {
                    "date": c.call_date,
                    "type": c.call_type,
                    "amount": float(c.amount),
                    "description": c.description,
                }
                for c in calls
            ],
            "distributions": [
                {
                    "date": d.distribution_date,
                    "type": d.distribution_type,
                    "amount": float(d.amount),
                    "description": d.description,
                }
                for d in dists
            ],
            "adjustments": [
                {
                    "date": a.adjustment_date,
                    "type": a.adjustment_type,
                    "amount": float(a.amount),
                    "description": a.description,
                }
                for a in adjs
            ],
            "metrics": {
                "PIC": float(pic),
                "DPI": dpi,
                "IRR": irr,
            },
        }
    finally:
        db.close()
