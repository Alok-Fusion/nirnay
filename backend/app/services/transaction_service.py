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
from typing import Dict, Any, List
from datetime import datetime
from backend.app.ai.orchestrator.graph import create_decision_graph

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
        
        # 5. Call AI LangGraph Orchestrator
        graph = create_decision_graph()
        initial_state = {
            "transaction_id": str(transaction.id),
            "raw_transaction_data": transaction_data,
            "raw_customer_id": user_id,
            "messages": [],
            "current_agent": "ContextIntelligenceAgent",
            "next_agent": "ContextIntelligenceAgent"
        }
        
        config = {"configurable": {"thread_id": str(transaction.id)}}
        
        try:
            result = graph.invoke(initial_state, config=config)
        except Exception as e:
            logger.error(f"LangGraph execution failed: {e}")
            result = initial_state
            result["decision_result"] = {"final_decision": "ESCALATE_TO_HUMAN", "decision_reason": "AI System Error"}
        
        context_data = result.get("context", {})
        ml_risk = context_data.get("ml_risk", {}) if isinstance(context_data, dict) else (context_data.ml_risk.model_dump() if hasattr(context_data, 'ml_risk') else {})
        decision_result = result.get("decision_result", {})
        evidence_report = result.get("evidence", {})
        
        if not isinstance(ml_risk, dict): ml_risk = {}
        if not isinstance(decision_result, dict): decision_result = {}
        
        # Extract evidence array for frontend
        evidence_list = []
        if isinstance(evidence_report, dict):
            evidences = evidence_report.get("evidences", [])
            for ev in evidences:
                if isinstance(ev, dict):
                    evidence_list.append(ev)
                else:
                    evidence_list.append(ev.model_dump())
        elif hasattr(evidence_report, "evidences"):
            for ev in evidence_report.evidences:
                evidence_list.append(ev.model_dump())
                
        # Combine risk evaluation for frontend response
        risk_evaluation = {
            "risk_score": ml_risk.get("risk_score", 0.0),
            "risk_level": ml_risk.get("risk_level", "Unknown"),
            "confidence": ml_risk.get("confidence", 0.0),
            "recommended_action": decision_result.get("final_decision", "Proceed"),
            "evidence": evidence_list
        }
        
        # 6. Create Risk Event
        risk_event = risk_event_repo.create(db, obj_in={
            "transaction_id": transaction.id,
            "risk_score": risk_evaluation["risk_score"],
            "risk_level": risk_evaluation["risk_level"],
            "confidence": risk_evaluation["confidence"],
            "recommended_action": decision_result.get("final_decision", "Proceed")
        })
        db.commit()
        
        # 7. Decide Next State based on ML output
        decision = decision_result.get("final_decision", "APPROVE_TRANSACTION")
        if decision == "APPROVE_TRANSACTION":
            transaction.status = TransactionState.APPROVED
            # Execute actual money movement logic here
            sender_account.balance -= request.amount
            message = decision_result.get("decision_reason", "Transfer Approved")
        elif decision in ["REQUEST_MORE_INFORMATION", "ESCALATE_TO_HUMAN"]:
            transaction.status = TransactionState.AWAITING_CUSTOMER_DECISION
            message = decision_result.get("decision_reason", "Transfer requires confirmation")
        else:
            transaction.status = TransactionState.REJECTED
            message = decision_result.get("decision_reason", "Transfer Rejected due to High Risk")
            
        db.commit()
        db.refresh(transaction)
        
        return TransferDecisionResponse(
            transaction=TransactionResponse.model_validate(transaction),
            risk_evaluation=risk_evaluation,
            message=message
        )
