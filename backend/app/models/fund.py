from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from app.db.session import Base

class Fund(Base):
    __tablename__ = "funds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    gp_name = Column(String(255))
    fund_type = Column(String(100))
    vintage_year = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
