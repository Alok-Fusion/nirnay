from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from backend.app.models.transaction import TransactionState, TransactionType

class TransferRequest(BaseModel):
    recipient_account_number: str = Field(..., description='Recipient account number')
    amount: float = Field(..., gt=0, description='Transfer amount')
    currency: str = Field(default='USD')

class TransactionResponse(BaseModel):
    id: int
    account_id: int
    recipient_id: Optional[int]
    amount: float
    currency: str
    status: TransactionState
    type: TransactionType
    created_at: datetime
    
    class Config:
        from_attributes = True

class TransferDecisionResponse(BaseModel):
    transaction: TransactionResponse
    risk_evaluation: Optional[Dict[str, Any]] = None
    message: str

