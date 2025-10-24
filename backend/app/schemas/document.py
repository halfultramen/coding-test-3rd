# backend/app/schemas/document.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DocumentOut(BaseModel):
    id: int
    fund_id: Optional[int]
    file_name: str
    file_path: Optional[str]
    parsing_status: str
    upload_date: datetime
    error_message: Optional[str] = None

    class Config:
        from_attributes = True

class DocumentStatusOut(BaseModel):
    document_id: int
    status: str
    error_message: Optional[str] = None
