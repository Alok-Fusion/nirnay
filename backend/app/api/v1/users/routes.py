from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.app.schemas.user import UserResponse
from backend.app.models.user import User
from backend.app.database.session import get_db
from backend.app.api.dependencies import get_current_user
from backend.app.repositories.user_repo import user_repo

router = APIRouter()

@router.get('/me', response_model=UserResponse)
def get_user_me(current_user: User = Depends(get_current_user)):
    return current_user
