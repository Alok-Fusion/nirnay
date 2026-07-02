from sqlalchemy.orm import Session
from backend.app.models.account import Account
from backend.app.repositories.base import BaseRepository
from typing import Optional, List

class AccountRepository(BaseRepository[Account]):
    def get_by_account_number(self, db: Session, account_number: str) -> Optional[Account]:
        return db.query(Account).filter(Account.account_number == account_number).first()
        
    def get_by_user_id(self, db: Session, user_id: int) -> List[Account]:
        return db.query(Account).filter(Account.user_id == user_id).all()

account_repo = AccountRepository(Account)

