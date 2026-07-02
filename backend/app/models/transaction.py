import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database.base import Base

class TransactionState(str, enum.Enum):
    INITIATED = "Initiated"
    VALIDATION = "Validation"
    RISK_ANALYSIS = "Risk Analysis"
    AWAITING_CUSTOMER_DECISION = "Awaiting Customer Decision"
    APPROVED = "Approved"
    COMPLETED = "Completed"
    REJECTED = "Rejected"

class TransactionType(str, enum.Enum):
    TRANSFER = "Transfer"
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("recipients.id"), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    status = Column(Enum(TransactionState), default=TransactionState.INITIATED, nullable=False)
    type = Column(Enum(TransactionType), default=TransactionType.TRANSFER, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    account = relationship("Account", foreign_keys=[account_id], back_populates="transactions_sent")
    recipient = relationship("Recipient", foreign_keys=[recipient_id], back_populates="transactions_received")
    risk_event = relationship("RiskEvent", back_populates="transaction", uselist=False, cascade="all, delete-orphan")
