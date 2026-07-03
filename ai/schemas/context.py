from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class CustomerProfile(BaseModel):
    user_id: int
    email: str
    full_name: str
    role: str

class TransactionContext(BaseModel):
    transaction_id: str
    amount: float
    currency: str
    type: str

class BehaviorProfile(BaseModel):
    avg_transaction_amount: float
    frequent_categories: List[str]
    last_updated: str

class RecipientInfo(BaseModel):
    recipient_id: Optional[int] = None
    account_number_masked: str
    bank_code: str
    name: str
    is_trusted: bool
    is_new: bool = False

class MerchantInfo(BaseModel):
    merchant_id: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    reputation_score: Optional[float] = None

class MLRiskResult(BaseModel):
    risk_score: float
    risk_level: str
    confidence: float
    reason_codes: List[str]
    features: Dict[str, Any]
    shap_values: Optional[List[Dict[str, Any]]] = None

class DecisionContext(BaseModel):
    """Normalized context created by Context Intelligence Agent."""
    customer: CustomerProfile
    transaction: TransactionContext
    behavior: BehaviorProfile
    recipient: Optional[RecipientInfo] = None
    merchant: Optional[MerchantInfo] = None
    ml_risk: MLRiskResult
    historical_context: Optional[Dict[str, Any]] = None
