# backend/app/api/endpoints/chat.py
from fastapi import APIRouter, Depends, HTTPException, Body
from app.schemas.chat import ChatQuery, ConversationOut, ChatMessageOut
from app.services import query_engine
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.models.chat import Conversation, ChatMessage
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/chat/query")
async def chat_query(payload: ChatQuery):
    try:
        print(f"[DEBUG] Chat query received: query='{payload.query}', fund_id={payload.fund_id}")
        result = query_engine.handle_query(payload.query, fund_id=payload.fund_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create new conversation
@router.post("/chat/conversations", response_model=ConversationOut)
def create_conversation(fund_id: int | None = Body(None), db: Session = Depends(get_db)):
    conv_id = str(uuid.uuid4())
    conv = Conversation(fund_id=fund_id, conversation_id=conv_id)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return ConversationOut(
        conversation_id=conv.conversation_id,
        fund_id=conv.fund_id,
        messages=[],
        created_at=conv.created_at,
        updated_at=conv.updated_at
    )

# Get conversation & messages
@router.get("/chat/conversations/{conversation_id}", response_model=ConversationOut)
def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages_out = []
    for m in conv.messages:
        messages_out.append(ChatMessageOut(role=m.role, content=m.content, timestamp=m.timestamp))

    return ConversationOut(
        conversation_id=conv.conversation_id,
        fund_id=conv.fund_id,
        messages=messages_out,
        created_at=conv.created_at,
        updated_at=conv.updated_at
    )

# Append message to conversation (optional helper)
@router.post("/chat/conversations/{conversation_id}/messages")
def append_message(conversation_id: str, role: str = Body(...), content: str = Body(...), db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    msg = ChatMessage(conversation_id=conv.id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return {"message": "ok"}
