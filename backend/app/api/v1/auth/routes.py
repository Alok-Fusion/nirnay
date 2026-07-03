from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.schemas.user import UserCreate, UserResponse
from backend.app.schemas.token import Token
from backend.app.database.session import get_db
from backend.app.services.auth_service import AuthService
from pydantic import BaseModel

class RefreshTokenRequest(BaseModel):
    refresh_token: str

router = APIRouter()

@router.post('/register', response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register_user(db, user_in)

@router.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return AuthService.authenticate(db, form_data.username, form_data.password)

@router.post('/refresh', response_model=Token)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    return AuthService.refresh(db, request.refresh_token)

