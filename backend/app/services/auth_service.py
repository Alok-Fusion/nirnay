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
        db.commit()
        logger.info(f"User registered successfully: {user.email}")
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
