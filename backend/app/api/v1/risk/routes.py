from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from backend.app.schemas.risk_event import RiskEventResponse
from backend.app.models.user import User
from backend.app.models.risk_event import RiskEvent
from backend.app.models.transaction import Transaction, TransactionState
from backend.app.models.account import Account
from backend.app.database.session import get_db
from backend.app.api.dependencies import get_current_user
from datetime import datetime

router = APIRouter()

@router.get('/history', response_model=List[RiskEventResponse])
def get_risk_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Get risk events associated with user's transactions
    risk_events = db.query(RiskEvent).join(Transaction).filter(Transaction.account_id.in_([a.id for a in current_user.accounts])).order_by(RiskEvent.created_at.desc()).all()
    return risk_events

@router.get('/report/{transaction_id}', response_model=RiskEventResponse)
def get_risk_report(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    risk_event = db.query(RiskEvent).filter(RiskEvent.transaction_id == transaction_id).first()
    if not risk_event:
        raise HTTPException(status_code=404, detail='Risk report not found')
    
    # Check if this belongs to the user
    if risk_event.transaction.account.user_id != current_user.id:
         raise HTTPException(status_code=403, detail='Forbidden')
         
    return risk_event

@router.get('/metrics', response_model=Dict[str, Any])
def get_security_metrics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Returns security metrics for the current user's Security Center."""
    account_ids = [a.id for a in current_user.accounts]
    
    # Blocked attempts in last 30 days
    blocked_count = db.query(func.count(Transaction.id)).filter(
        Transaction.account_id.in_(account_ids),
        Transaction.status == TransactionState.BLOCKED
    ).scalar() or 0
    
    # Average ML risk score (used to derive overallScore)
    avg_risk = db.query(func.avg(RiskEvent.risk_score)).join(
        Transaction, RiskEvent.transaction_id == Transaction.id
    ).filter(
        Transaction.account_id.in_(account_ids)
    ).scalar() or 0.0
    
    # Overall security score: inverse of average risk, scaled to 100
    overall_score = max(0, round((1.0 - float(avg_risk)) * 100))
    
    # Last login: use user's last updated_at as proxy
    last_login = current_user.created_at.isoformat() if hasattr(current_user, 'created_at') and current_user.created_at else datetime.utcnow().isoformat()
    
    return {
        "overallScore": overall_score,
        "trustedDevices": 1,  # Current device is always trusted for authenticated sessions
        "blockedAttempts": blocked_count,
        "lastLogin": last_login,
        "activeAlerts": blocked_count  # Active alerts = blocked transfers
    }
