# backend/app/schemas/chat.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatQuery(BaseModel):
    query: str
    fund_id: Optional[int] = None
    conversation_id: Optional[str] = None

class ChatMessageOut(BaseModel):
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True

class ConversationOut(BaseModel):
    conversation_id: str
    fund_id: Optional[int]
    messages: List[ChatMessageOut]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
