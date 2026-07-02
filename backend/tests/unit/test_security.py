from backend.app.core.security import get_password_hash, verify_password, create_access_token
from jose import jwt
from backend.app.core.config import settings

def test_password_hashing():
    password = 'securepassword123'
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password('wrongpassword', hashed)

def test_create_access_token():
    subject = '123'
    token = create_access_token(subject)
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload['sub'] == subject
    assert payload['type'] == 'access'

