from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.sql import func
from backend.app.database.base import Base

class ScamPattern(Base):
    __tablename__ = 'scam_patterns'

    id = Column(Integer, primary_key=True, index=True)
    pattern_description = Column(String, nullable=False)
    risk_weight = Column(Float, nullable=False)
    keywords = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

