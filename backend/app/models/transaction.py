from sqlalchemy import Column, Integer, String, Date, Numeric, Boolean, ForeignKey, TIMESTAMP, func
from app.db.session import Base

class CapitalCall(Base):
    __tablename__ = "capital_calls"
    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("funds.id"))
    call_date = Column(Date, nullable=False)
    call_type = Column(String(100))
    amount = Column(Numeric(15,2), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Distribution(Base):
    __tablename__ = "distributions"
    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("funds.id"))
    distribution_date = Column(Date, nullable=False)
    distribution_type = Column(String(100))
    is_recallable = Column(Boolean, default=False)
    amount = Column(Numeric(15,2), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Adjustment(Base):
    __tablename__ = "adjustments"
    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("funds.id"))
    adjustment_date = Column(Date, nullable=False)
    adjustment_type = Column(String(100))
    category = Column(String(100))
    amount = Column(Numeric(15,2), nullable=False)
    is_contribution_adjustment = Column(Boolean, default=False)
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
