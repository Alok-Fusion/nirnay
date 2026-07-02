from sqlalchemy.orm import Session
from backend.app.models.transaction import Transaction
from backend.app.repositories.base import BaseRepository
from typing import List

class TransactionRepository(BaseRepository[Transaction]):
    def get_by_account_id(self, db: Session, account_id: int) -> List[Transaction]:
        return db.query(Transaction).filter(Transaction.account_id == account_id).order_by(Transaction.created_at.desc()).all()

transaction_repo = TransactionRepository(Transaction)

