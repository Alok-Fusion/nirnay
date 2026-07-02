from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database.base import Base

class Feedback(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey('risk_events.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    feedback_text = Column(String, nullable=False)
    rating = Column(Integer, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    risk_event = relationship('RiskEvent', back_populates='feedback')

