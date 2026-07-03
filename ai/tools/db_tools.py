import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.database.session import SessionLocal
from backend.app.models.user import User
from backend.app.models.transaction import Transaction
from backend.app.models.recipient import Recipient
from backend.app.models.behavior_profile import BehaviorProfile

logger = logging.getLogger(__name__)

def get_customer_profile(user_id: int) -> Optional[Dict[str, Any]]:
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return {
                "user_id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value if hasattr(user.role, 'value') else str(user.role)
            }
    finally:
        db.close()
    return None

def get_behavior_profile(user_id: int) -> Optional[Dict[str, Any]]:
    db: Session = SessionLocal()
    try:
        profile = db.query(BehaviorProfile).filter(BehaviorProfile.user_id == user_id).first()
        if profile:
            return {
                "avg_transaction_amount": profile.avg_transaction_amount,
                "frequent_categories": profile.frequent_categories or [],
                "last_updated": str(profile.last_updated)
            }
        # Default behavior profile if none exists
        return {
            "avg_transaction_amount": 0.0,
            "frequent_categories": [],
            "last_updated": "never"
        }
    finally:
        db.close()

def get_recipient_info(recipient_id: int) -> Optional[Dict[str, Any]]:
    db: Session = SessionLocal()
    try:
        recipient = db.query(Recipient).filter(Recipient.id == recipient_id).first()
        if recipient:
            return {
                "recipient_id": recipient.id,
                "account_number_masked": "***" + str(recipient.account_number)[-4:] if recipient.account_number else "***",
                "bank_code": recipient.bank_code,
                "name": recipient.name,
                "is_trusted": recipient.is_trusted,
                "is_new": False # This would be calculated historically
            }
    finally:
        db.close()
    return None
