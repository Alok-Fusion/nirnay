from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.app.schemas.user import UserResponse
from backend.app.models.user import User
from backend.app.database.session import get_db
from backend.app.api.dependencies import get_current_admin_user

router = APIRouter()

@router.get('/customers', response_model=List[UserResponse])
def get_customers(db: Session = Depends(get_db), admin_user: User = Depends(get_current_admin_user)):
    return db.query(User).filter(User.role == 'Customer').all()

@router.get('/system-stats')
def get_system_stats(db: Session = Depends(get_db), admin_user: User = Depends(get_current_admin_user)):
    user_count = db.query(User).count()
    return {'total_users': user_count, 'status': 'Healthy'}

