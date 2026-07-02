from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.schemas.recipient import RecipientCreate, RecipientResponse
from backend.app.models.user import User
from backend.app.models.recipient import Recipient
from backend.app.database.session import get_db
from backend.app.api.dependencies import get_current_user

router = APIRouter()

@router.get('', response_model=List[RecipientResponse])
def get_recipients(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Recipient).filter(Recipient.user_id == current_user.id).all()

@router.post('', response_model=RecipientResponse)
def create_recipient(recipient_in: RecipientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if recipient already exists for user
    existing = db.query(Recipient).filter(
        Recipient.user_id == current_user.id,
        Recipient.account_number == recipient_in.account_number
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail='Recipient already exists')
        
    new_recipient = Recipient(
        user_id=current_user.id,
        account_number=recipient_in.account_number,
        bank_code=recipient_in.bank_code,
        name=recipient_in.name,
        is_trusted=recipient_in.is_trusted
    )
    db.add(new_recipient)
    db.commit()
    db.refresh(new_recipient)
    return new_recipient

