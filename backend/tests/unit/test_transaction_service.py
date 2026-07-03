from backend.app.schemas.transaction import TransferRequest
from backend.app.services.transaction_orchestrator import TransactionOrchestrator
from backend.app.models.transaction import TransactionState
from backend.app.core.exceptions import BadRequestException, NotFoundException
import pytest

# Note: Since these tests require DB interaction and mock repositories,
# in a real setup we would use pytest-mock to mock `account_repo`, `transaction_repo`, etc.

def test_transfer_validation_fails_no_account(db):
    request = TransferRequest(recipient_account_number="12345", amount=100.0)
    with pytest.raises(NotFoundException):
        # User 9999 has no accounts
        TransactionOrchestrator.process(db, user_id=9999, request=request)
