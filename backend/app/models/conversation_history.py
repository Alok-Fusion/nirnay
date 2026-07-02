from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from backend.app.database.base import Base

class ConversationHistory(Base):
    __tablename__ = 'conversation_histories'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_id = Column(String, index=True, nullable=False)
    message = Column(String, nullable=False)
    sender = Column(String, nullable=False) # 'User' or 'Bot'
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

