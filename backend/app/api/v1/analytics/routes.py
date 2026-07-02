from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.schemas.analytics import AnalyticsResponse, CategorySpending
from backend.app.models.user import User
from backend.app.models.transaction import Transaction, TransactionState, TransactionType
from backend.app.database.session import get_db
from backend.app.api.dependencies import get_current_user

router = APIRouter()

@router.get('/summary', response_model=AnalyticsResponse)
def get_analytics_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Mocking analytics aggregation for MVP
    # In reality, this would group by category (which might be in merchant model)
    total_spent = db.query(func.sum(Transaction.amount)).filter(
        Transaction.account_id.in_([a.id for a in current_user.accounts]),
        Transaction.status == TransactionState.COMPLETED,
        Transaction.type == TransactionType.TRANSFER
    ).scalar() or 0.0

    return AnalyticsResponse(
        total_spent=total_spent,
        categories=[CategorySpending(category='Shopping', amount=total_spent)],
        risk_distribution={'Low': 5, 'Medium': 2, 'High': 0}
    )

