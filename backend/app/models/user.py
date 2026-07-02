import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database.base import Base

class UserRole(str, enum.Enum):
    CUSTOMER = "Customer"
    ADMIN = "Admin"
    DEMO = "Demo"
    RISK_ANALYST = "Risk Analyst"
    SUPPORT = "Support"
    AUDITOR = "Auditor"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    # Hashed using Argon2id
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    recipients = relationship("Recipient", back_populates="user", cascade="all, delete-orphan")
    behavior_profile = relationship("BehaviorProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
