from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.schemas.transaction import TransferRequest, TransferDecisionResponse
from backend.app.models.user import User
from backend.app.database.session import get_db
from backend.app.api.dependencies import get_current_user
from backend.app.services.transaction_service import TransactionService

router = APIRouter()

@router.post('/transfer', response_model=TransferDecisionResponse)
def transfer_money(request: TransferRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TransactionService.transfer(db, current_user.id, request)

