from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func
from backend.app.database.base import Base

class DashboardMetric(Base):
    __tablename__ = 'dashboard_metrics'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    metric_name = Column(String, index=True, nullable=False)
    value = Column(JSON, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

