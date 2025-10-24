from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FundCreate(BaseModel):
    name: str
    gp_name: Optional[str] = None
    fund_type: Optional[str] = None
    vintage_year: Optional[int] = None

class FundOut(FundCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 
