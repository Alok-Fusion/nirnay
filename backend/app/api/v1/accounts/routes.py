from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.app.schemas.account import AccountResponse
from backend.app.models.user import User
from backend.app.database.session import get_db
from backend.app.api.dependencies import get_current_user
from backend.app.repositories.account_repo import account_repo

router = APIRouter()

@router.get('/summary', response_model=List[AccountResponse])
def get_account_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return account_repo.get_by_user_id(db, current_user.id)
