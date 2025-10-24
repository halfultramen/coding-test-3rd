from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Text, func
from app.db.session import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("funds.id"), nullable=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=True)
    upload_date = Column(TIMESTAMP, server_default=func.now())
    parsing_status = Column(String(50), default="pending")
    error_message = Column(Text, nullable=True)
