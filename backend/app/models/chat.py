# backend/app/models/chat.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, nullable=True)
    conversation_id = Column(String(64), unique=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    messages = relationship("ChatMessage", back_populates="conversation", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String(32))  # "user" or "assistant" or "system"
    content = Column(Text)
    timestamp = Column(TIMESTAMP, server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")
