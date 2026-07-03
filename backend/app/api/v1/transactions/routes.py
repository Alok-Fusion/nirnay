from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.schemas.transaction import TransferRequest, TransferDecisionResponse, TransactionResponse
from backend.app.models.user import User
from backend.app.models.transaction import Transaction
from backend.app.models.account import Account
from typing import List
from backend.app.database.session import get_db
from backend.app.api.dependencies import get_current_user
from backend.app.services.transaction_service import TransactionService

router = APIRouter()

@router.post('/transfer', response_model=TransferDecisionResponse)
def transfer_money(request: TransferRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TransactionService.transfer(db, current_user.id, request)

@router.get('/history', response_model=List[TransactionResponse])
def get_transaction_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transactions = db.query(Transaction).join(Account, Transaction.account_id == Account.id).filter(Account.user_id == current_user.id).order_by(Transaction.created_at.desc()).all()
    
    # Map extra fields for the frontend
    for tx in transactions:
        tx.recipientName = tx.recipient.name if tx.recipient else "Unknown"
        tx.aiRiskScore = tx.risk_event.risk_score if tx.risk_event else 0.0
        
    return transactions

