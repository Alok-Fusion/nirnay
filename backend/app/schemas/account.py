from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccountBase(BaseModel):
    account_number: str
    currency: str = 'USD'
    status: str = 'Active'

class AccountResponse(AccountBase):
    id: int
    user_id: int
    balance: float
    created_at: datetime

    class Config:
        from_attributes = True

