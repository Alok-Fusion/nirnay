from sqlalchemy.orm import Session
from backend.app.repositories.user_repo import user_repo
from backend.app.schemas.user import UserCreate
from backend.app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from backend.app.core.exceptions import CredentialsException, BadRequestException
import logging

logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def register_user(db: Session, user_in: UserCreate):
        if user_repo.get_by_email(db, email=user_in.email):
            logger.warning(f"Registration failed: Email {user_in.email} already registered.")
            raise BadRequestException("Email already registered")
        
        user_data = user_in.model_dump(exclude={"password"})
        user_data["password_hash"] = get_password_hash(user_in.password)
        
        user = user_repo.create(db, obj_in=user_data)
        
        # Create a starting bank account for the customer
        import random
        from backend.app.models.account import Account
        
        acc_number = f"ACC-{random.randint(100000, 999999)}"
        # Ensure unique
        while db.query(Account).filter(Account.account_number == acc_number).first() is not None:
            acc_number = f"ACC-{random.randint(100000, 999999)}"
            
        account = Account(
            user_id=user.id,
            account_number=acc_number,
            balance=150000.0,
            currency="USD",
            status="Active"
        )
        db.add(account)
        db.flush()
        
        # Initialize BehaviorProfile
        from backend.app.models.behavior_profile import BehaviorProfile
        profile = BehaviorProfile(
            user_id=user.id,
            avg_transaction_amount=0.0,
            transaction_count=0,
            average_daily_transactions=0.0,
            trusted_recipients=[],
            known_devices=[],
            known_locations=[],
            average_balance=150000.0,
            historical_risk=0.0,
            trust_score=50,
            trust_level="NEW"
        )
        db.add(profile)
        db.commit()
        logger.info(f"User registered successfully with Account {acc_number} and BehaviorProfile: {user.email}")
        return user

    @staticmethod
    def authenticate(db: Session, email: str, password: str):
        user = user_repo.get_by_email(db, email=email)
        if not user:
            logger.warning(f"Authentication failed: User {email} not found.")
            raise CredentialsException("Incorrect email or password")
        if not verify_password(password, user.password_hash):
            logger.warning(f"Authentication failed: Incorrect password for {email}.")
            raise CredentialsException("Incorrect email or password")
        
        logger.info(f"User authenticated: {email}")
        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 1800 # 30 mins
        }
        
    @staticmethod
    def refresh(db: Session, token: str):
        from backend.app.core.security import decode_token
        try:
            payload = decode_token(token)
            if payload.type != "refresh":
                raise CredentialsException("Invalid token type")
            user_id = payload.sub
            if not user_id:
                raise CredentialsException("Invalid token")
                
            user = user_repo.get(db, id=int(user_id))
            if not user:
                raise CredentialsException("User not found")
                
            access_token = create_access_token(subject=user.id)
            refresh_token = create_refresh_token(subject=user.id)
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": 1800
            }
        except Exception as e:
            logger.error(f"Refresh failed: {e}")
            raise CredentialsException("Could not validate credentials")
