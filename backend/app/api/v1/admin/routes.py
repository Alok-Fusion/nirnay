from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.schemas.user import UserResponse
from backend.app.models.user import User
from backend.app.models.behavior_profile import BehaviorProfile
from backend.app.database.session import get_db
from backend.app.api.dependencies import get_current_admin_user
from pydantic import BaseModel

router = APIRouter()

class BehaviorOverrideRequest(BaseModel):
    trust_score: int
    trust_level: str

@router.get('/customers', response_model=List[UserResponse])
def get_customers(db: Session = Depends(get_db), admin_user: User = Depends(get_current_admin_user)):
    return db.query(User).filter(User.role == 'Customer').all()

@router.get('/system-stats')
def get_system_stats(db: Session = Depends(get_db), admin_user: User = Depends(get_current_admin_user)):
    from backend.app.models.transaction import Transaction
    user_count = db.query(User).count()
    tx_count = db.query(Transaction).count()
    return {
        'total_users': user_count, 
        'total_transactions': tx_count,
        'status': 'Healthy',
        'ai_confidence': 96.4,
        'system_uptime': '99.99%'
    }

@router.post('/customers/{customer_id}/suspend', response_model=UserResponse)
def suspend_customer(customer_id: int, db: Session = Depends(get_db), admin_user: User = Depends(get_current_admin_user)):
    customer = db.query(User).filter(User.id == customer_id, User.role == 'Customer').first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.is_active = False
    db.commit()
    db.refresh(customer)
    return customer

@router.post('/customers/{customer_id}/activate', response_model=UserResponse)
def activate_customer(customer_id: int, db: Session = Depends(get_db), admin_user: User = Depends(get_current_admin_user)):
    customer = db.query(User).filter(User.id == customer_id, User.role == 'Customer').first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.is_active = True
    db.commit()
    db.refresh(customer)
    return customer

@router.post('/customers/{customer_id}/override-behavior')
def override_behavior(customer_id: int, request: BehaviorOverrideRequest, db: Session = Depends(get_db), admin_user: User = Depends(get_current_admin_user)):
    customer = db.query(User).filter(User.id == customer_id, User.role == 'Customer').first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    profile = db.query(BehaviorProfile).filter(BehaviorProfile.user_id == customer_id).first()
    if not profile:
        profile = BehaviorProfile(
            user_id=customer_id,
            avg_transaction_amount=0.0,
            transaction_count=0,
            average_daily_transactions=0.0,
            trusted_recipients=[],
            known_devices=[],
            known_locations=[]
        )
        db.add(profile)
        
    profile.trust_score = request.trust_score
    profile.trust_level = request.trust_level
    db.commit()
    return {"message": "Customer behavior profile updated successfully"}


