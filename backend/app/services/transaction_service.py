from sqlalchemy.orm import Session
from backend.app.schemas.transaction import TransferRequest, TransactionResponse, TransferDecisionResponse
from backend.app.models.transaction import Transaction, TransactionState, TransactionType
from backend.app.models.risk_event import RiskEvent
from backend.app.models.account import Account
from backend.app.models.recipient import Recipient
from backend.app.repositories.transaction_repo import transaction_repo
from backend.app.repositories.account_repo import account_repo
from backend.app.repositories.risk_event_repo import risk_event_repo
from backend.app.services.ml_service import ml_service
from backend.app.core.exceptions import BadRequestException, NotFoundException
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class TransactionService:
    @staticmethod
    def transfer(db: Session, user_id: int, request: TransferRequest) -> TransferDecisionResponse:
        # 1. Validation (Customer Account)
        accounts = account_repo.get_by_user_id(db, user_id)
        if not accounts:
            raise NotFoundException("Customer has no active accounts")
        sender_account = accounts[0] # Simplification for MVP
        
        if sender_account.balance < request.amount:
            raise BadRequestException("Insufficient balance")
            
        # 2. Validation (Recipient)
        recipient = db.query(Recipient).filter(
            Recipient.user_id == user_id,
            Recipient.account_number == request.recipient_account_number
        ).first()
        
        if not recipient:
            raise BadRequestException("Recipient not found or not trusted")
            
        # 3. Create Transaction (INITIATED)
        transaction = transaction_repo.create(db, obj_in={
            "account_id": sender_account.id,
            "recipient_id": recipient.id,
            "amount": request.amount,
            "currency": request.currency,
            "status": TransactionState.INITIATED,
            "type": TransactionType.TRANSFER
        })
        db.commit()
        db.refresh(transaction)
        logger.info(f"Transaction {transaction.id} initiated by user {user_id}")
        
        # 4. Gather data for ML
        # Mocking joining of user/behavior data here for ML input
        transaction_data = {
            "transaction_id": str(transaction.id),
            "amount": request.amount,
            "sender_balance": sender_account.balance,
            "recipient_bank_code": recipient.bank_code,
            "is_trusted_recipient": recipient.is_trusted,
            "hour_of_day": datetime.now().hour,
            # In a full implementation, we'd add behavior profile features here
            "avg_transaction_amount": 500.0,
            "risk_label": 0 
        }
        
        # Move to RISK_ANALYSIS
        transaction.status = TransactionState.RISK_ANALYSIS
        db.commit()
        
        # 5. Call ML Service
        ml_result = ml_service.analyze_transaction(transaction_data)
        
        # 6. Create Risk Event
        risk_event = risk_event_repo.create(db, obj_in={
            "transaction_id": transaction.id,
            "risk_score": ml_result.get("risk_score", 0),
            "risk_level": ml_result.get("risk_level", "Unknown"),
            "confidence": ml_result.get("confidence", 0),
            "recommended_action": ml_result.get("recommended_action", "Proceed")
        })
        db.commit()
        
        # 7. Decide Next State based on ML output
        action = ml_result.get("recommended_action", "Proceed")
        if action == "Proceed":
            transaction.status = TransactionState.APPROVED
            # Execute actual money movement logic here
            sender_account.balance -= request.amount
            message = "Transfer Approved"
            # Next would be COMPLETED
        elif action == "Explain" or action == "Start Conversation":
            transaction.status = TransactionState.AWAITING_CUSTOMER_DECISION
            message = "Transfer requires confirmation"
        else:
            transaction.status = TransactionState.REJECTED
            message = "Transfer Rejected due to High Risk"
            
        db.commit()
        db.refresh(transaction)
        
        return TransferDecisionResponse(
            transaction=TransactionResponse.model_validate(transaction),
            risk_evaluation=ml_result,
            message=message
        )
