import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database.base import Base

class TransactionState(str, enum.Enum):
    INITIATED = "Initiated"
    VALIDATING = "Validating"
    CUSTOMER_CONTEXT_READY = "Customer Context Ready"
    FEATURE_ENGINEERING = "Feature Engineering"
    ML_ANALYSIS = "ML Analysis"
    RULE_ENGINE = "Rule Engine"
    AI_ANALYSIS = "AI Analysis"
    AI_POLICY = "AI Policy"
    CUSTOMER_VERIFICATION = "Customer Verification"
    AWAITING_CUSTOMER_RESPONSE = "Awaiting Customer Response"
    PENDING_DECISION = "Pending Decision"
    APPROVED = "Approved"
    STEP_UP_AUTHENTICATION = "Step Up Authentication"
    EXECUTING = "Executing"
    COMPLETED = "Completed"
    BLOCKED = "Blocked"
    CANCELLED = "Cancelled"
    FAILED = "Failed"

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
