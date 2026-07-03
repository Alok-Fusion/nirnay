import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.database.session import engine, SessionLocal
from backend.app.database.base import Base
import backend.app.models  # imports all models
from backend.app.models.user import User, UserRole
from backend.app.models.account import Account
from backend.app.models.recipient import Recipient
from backend.app.core.security import get_password_hash

def seed_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    email = "alok@example.com"
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        print(f"Creating user {email}...")
        user = User(
            email=email,
            full_name="Alok Kumar",
            password_hash=get_password_hash("password"),
            role=UserRole.CUSTOMER,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    account = db.query(Account).filter(Account.user_id == user.id).first()
    if not account:
        print("Creating account...")
        account = Account(
            user_id=user.id,
            account_number="CHK-9876543210",
            balance=250000.0,
            currency="USD",
            status="Active"
        )
        db.add(account)
        db.commit()
        
    recipient = db.query(Recipient).filter(Recipient.user_id == user.id).first()
    if not recipient:
        print("Creating recipient...")
        recipient = Recipient(
            user_id=user.id,
            name="John Doe",
            account_number="REC-123456",
            bank_code="BOA001",
            is_trusted=True
        )
        db.add(recipient)
        db.commit()
        
    from backend.app.models.behavior_profile import BehaviorProfile
    profile = db.query(BehaviorProfile).filter(BehaviorProfile.user_id == user.id).first()
    if not profile:
        print("Creating behavior profile...")
        profile = BehaviorProfile(
            user_id=user.id,
            avg_transaction_amount=120.0,
            transaction_count=8,
            average_daily_transactions=0.4,
            trusted_recipients=[1],
            known_devices=["Chrome/Windows"],
            known_locations=["India"],
            average_balance=250000.0,
            historical_risk=0.08,
            trust_score=72,
            trust_level="LEARNING"
        )
        db.add(profile)
        db.commit()
        
    print("Seed complete.")
    db.close()

if __name__ == "__main__":
    seed_db()
