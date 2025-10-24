from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class CapitalCallCreate(BaseModel):
    fund_id: int
    call_date: str
    call_type: Optional[str] = None
    amount: Decimal
    description: Optional[str] = None

class DistributionCreate(BaseModel):
    fund_id: int
    distribution_date: str
    distribution_type: Optional[str] = None
    is_recallable: Optional[bool] = False
    amount: Decimal
    description: Optional[str] = None

class AdjustmentCreate(BaseModel):
    fund_id: int
    adjustment_date: str
    adjustment_type: Optional[str] = None
    category: Optional[str] = None
    amount: Decimal
    is_contribution_adjustment: Optional[bool] = False
    description: Optional[str] = None
