from pydantic import BaseModel
from typing import Dict, Any, List

class CategorySpending(BaseModel):
    category: str
    amount: float

class AnalyticsResponse(BaseModel):
    total_spent: float
    categories: List[CategorySpending]
    risk_distribution: Dict[str, int]

