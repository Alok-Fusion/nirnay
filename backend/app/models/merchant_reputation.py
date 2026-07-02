from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from backend.app.database.base import Base

class MerchantReputation(Base):
    __tablename__ = 'merchant_reputations'

    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    risk_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

