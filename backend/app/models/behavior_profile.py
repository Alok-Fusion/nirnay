from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, JSON, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database.base import Base

class BehaviorProfile(Base):
    __tablename__ = "behavior_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    avg_transaction_amount = Column(Float, default=0.0)
    frequent_categories = Column(JSON, nullable=True)
    
    # Enriched fields for Phase 5.5 Behavior Profile / Digital Twin
    transaction_count = Column(Integer, default=0)
    average_daily_transactions = Column(Float, default=0.0)
    preferred_transfer_hour = Column(Integer, nullable=True)
    trusted_recipients = Column(JSON, default=list, nullable=True)
    known_devices = Column(JSON, default=list, nullable=True)
    known_locations = Column(JSON, default=list, nullable=True)
    average_balance = Column(Float, default=0.0)
    last_transaction = Column(DateTime(timezone=True), nullable=True)
    historical_risk = Column(Float, default=0.0)
    trust_score = Column(Integer, default=50)
    trust_level = Column(String, default="NEW") # NEW, LEARNING, ESTABLISHED, TRUSTED
    
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="behavior_profile")
