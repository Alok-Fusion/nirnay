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

@router.get('/security')
def get_user_security(current_user: User = Depends(get_current_user)):
    # Calculate mock metrics based on real user data or return static values for MVP
    return {
        "overallScore": 92,
        "trustedDevices": 1,
        "blockedAttempts": 0,
        "lastLogin": current_user.created_at.isoformat(),
        "activeAlerts": 0
    }

@router.get('/me/behavior')
def get_user_behavior(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from backend.app.models.behavior_profile import BehaviorProfile
    profile = db.query(BehaviorProfile).filter(BehaviorProfile.user_id == current_user.id).first()
    
    if not profile:
        # Create default profile if somehow missing
        profile = BehaviorProfile(
            user_id=current_user.id,
            avg_transaction_amount=0.0,
            transaction_count=0,
            average_daily_transactions=0.0,
            trusted_recipients=[],
            known_devices=[],
            known_locations=[],
            average_balance=0.0,
            historical_risk=0.0,
            trust_score=50,
            trust_level="NEW"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        
    return {
        "avg_transaction_amount": profile.avg_transaction_amount,
        "transaction_count": profile.transaction_count,
        "average_daily_transactions": profile.average_daily_transactions,
        "preferred_transfer_hour": profile.preferred_transfer_hour,
        "trusted_recipients": profile.trusted_recipients or [],
        "known_devices": profile.known_devices or [],
        "known_locations": profile.known_locations or [],
        "average_balance": profile.average_balance,
        "historical_risk": profile.historical_risk,
        "trust_score": profile.trust_score,
        "trust_level": profile.trust_level,
        "last_updated": profile.last_updated.isoformat() if profile.last_updated else None
    }
