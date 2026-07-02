from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database.base import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_number = Column(String, unique=True, index=True, nullable=False)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    status = Column(String, default="Active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="accounts")
    transactions_sent = relationship("Transaction", foreign_keys="[Transaction.account_id]", back_populates="account")
