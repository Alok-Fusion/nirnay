from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from backend.app.database.base import Base
from backend.app.core.config import settings

class Recipient(Base):
    __tablename__ = "recipients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Encrypted sensitive field
    account_number = Column(EncryptedType(String, settings.SECRET_KEY, AesEngine, 'pkcs5'), nullable=False)
    bank_code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    is_trusted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="recipients")
    transactions_received = relationship("Transaction", foreign_keys="[Transaction.recipient_id]", back_populates="recipient")
