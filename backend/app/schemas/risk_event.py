from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class RiskEventBase(BaseModel):
    transaction_id: int
    risk_score: float
    risk_level: str
    confidence: float
    recommended_action: str
    reason_codes: Optional[List[str]] = None

class RiskEventResponse(RiskEventBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

