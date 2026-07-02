from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database.base import Base

class RiskEvent(Base):
    __tablename__ = "risk_events"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False, unique=True)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    reason_codes = Column(JSON, nullable=True)
    features = Column(JSON, nullable=True)
    recommended_action = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    transaction = relationship("Transaction", back_populates="risk_event")
    feedback = relationship("Feedback", back_populates="risk_event", uselist=False, cascade="all, delete-orphan")
