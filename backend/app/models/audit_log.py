from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from backend.app.database.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Nullable for system events
    action = Column(String, index=True, nullable=False)
    entity = Column(String, index=True, nullable=True) # e.g. "Transaction", "User"
    entity_id = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String, nullable=True)
    correlation_id = Column(String, index=True, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
