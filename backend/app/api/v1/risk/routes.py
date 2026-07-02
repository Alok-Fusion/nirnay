from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.schemas.risk_event import RiskEventResponse
from backend.app.models.user import User
from backend.app.models.risk_event import RiskEvent
from backend.app.models.transaction import Transaction
from backend.app.database.session import get_db
from backend.app.api.dependencies import get_current_user

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

