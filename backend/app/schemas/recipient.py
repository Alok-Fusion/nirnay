from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RecipientBase(BaseModel):
    account_number: str
    bank_code: str
    name: str
    is_trusted: bool = False

class RecipientCreate(RecipientBase):
    pass

class RecipientResponse(RecipientBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

