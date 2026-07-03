from sqlalchemy.orm import Session
from backend.app.schemas.transaction import TransferRequest, TransactionResponse, TransferDecisionResponse
from backend.app.models.transaction import Transaction, TransactionState, TransactionType
from backend.app.models.risk_event import RiskEvent
from backend.app.models.account import Account
from backend.app.models.recipient import Recipient
from backend.app.repositories.transaction_repo import transaction_repo
from backend.app.repositories.account_repo import account_repo
from backend.app.repositories.risk_event_repo import risk_event_repo
from backend.app.core.exceptions import BadRequestException, NotFoundException
from ai.orchestrator.graph import create_decision_graph
from backend.app.ai.decision.rule_engine import RuleEngine
from backend.app.ai.features.generator import FeatureGenerator
import logging
from datetime import datetime
import time

logger = logging.getLogger(__name__)

class TransactionOrchestrator:
    @staticmethod
    def _update_state(db: Session, transaction: Transaction, state: TransactionState):
        transaction.status = state
        db.commit()
        logger.info(f"Transaction {transaction.id} transitioned to state: {state}")
        # In a real async enterprise system, we'd fire events here.
        # For this synchronous API, we just persist state.

    @staticmethod
    def process(db: Session, user_id: int, request: TransferRequest) -> TransferDecisionResponse:
        logger.info(f"Initiating transaction workflow for user {user_id}")
        
        # 1. INITIATED -> VALIDATING
        accounts = account_repo.get_by_user_id(db, user_id)
        if not accounts:
            raise NotFoundException("Customer has no active accounts")
        sender_account = accounts[0]
        
        recipient = db.query(Recipient).filter(
            Recipient.user_id == user_id,
            Recipient.account_number == request.recipient_account_number
        ).first()
        
        if not recipient:
            raise BadRequestException("Recipient not found")

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
        
        TransactionOrchestrator._update_state(db, transaction, TransactionState.VALIDATING)
        
        if sender_account.balance < request.amount:
            TransactionOrchestrator._update_state(db, transaction, TransactionState.FAILED)
            raise BadRequestException("Insufficient balance")

        # 2. CUSTOMER_CONTEXT_READY
        TransactionOrchestrator._update_state(db, transaction, TransactionState.CUSTOMER_CONTEXT_READY)
        transaction_data = FeatureGenerator.generate(db, user_id, sender_account.id, recipient.id, request.amount)
        transaction_data["transaction_id"] = str(transaction.id)
        transaction_data["amount"] = request.amount
        transaction_data["recipient_bank_code"] = recipient.bank_code
        
        # 3. FEATURE_ENGINEERING -> ML_ANALYSIS
        TransactionOrchestrator._update_state(db, transaction, TransactionState.FEATURE_ENGINEERING)
        # (Mock feature engineering delay)
        TransactionOrchestrator._update_state(db, transaction, TransactionState.ML_ANALYSIS)
        
        # 4. RULE_ENGINE
        TransactionOrchestrator._update_state(db, transaction, TransactionState.RULE_ENGINE)
        rule_result, rule_reason, scam_type = RuleEngine.evaluate(transaction_data, request.amount)
        
        if rule_result == "HARD_BLOCK":
            TransactionOrchestrator._update_state(db, transaction, TransactionState.BLOCKED)
            return TransferDecisionResponse(
                transaction=TransactionResponse.model_validate(transaction),
                risk_evaluation={
                    "risk_score": 1.0,
                    "risk_level": "High",
                    "confidence": 1.0,
                    "recommended_action": "BLOCK",
                    "scam_type": scam_type,
                    "reasoning": [rule_reason],
                    "evidence": [{"feature": "Rule Engine", "value": rule_reason, "shap_value": 1.0}]
                },
                message=rule_reason
            )
            
        if rule_result == "SAFE":
            TransactionOrchestrator._update_state(db, transaction, TransactionState.APPROVED)
            TransactionOrchestrator._update_state(db, transaction, TransactionState.STEP_UP_AUTHENTICATION)
            
            return TransferDecisionResponse(
                transaction=TransactionResponse.model_validate(transaction),
                risk_evaluation={
                    "risk_score": 0.0,
                    "risk_level": "Low",
                    "confidence": 1.0,
                    "recommended_action": "APPROVE_TRANSACTION",
                    "scam_type": None,
                    "reasoning": [rule_reason],
                    "evidence": [{"feature": "Rule Engine", "value": rule_reason, "shap_value": 0.0}]
                },
                message=rule_reason
            )
            
        # 5. AI_ANALYSIS (if rule_result == "SUSPICIOUS")
        TransactionOrchestrator._update_state(db, transaction, TransactionState.AI_ANALYSIS)
        
        graph = create_decision_graph()
        initial_state = {
            "transaction_id": str(transaction.id),
            "raw_transaction_data": transaction_data,
            "raw_customer_id": user_id,
            "scam_type": scam_type,  # Thread scam context into AI graph
            "rule_reason": rule_reason,
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

        TransactionOrchestrator._update_state(db, transaction, TransactionState.AI_POLICY)
        
        context_data = result.get("context", {})
        ml_risk = context_data.get("ml_risk", {}) if isinstance(context_data, dict) else (context_data.ml_risk.model_dump() if hasattr(context_data, 'ml_risk') else {})
        decision_result = result.get("decision_result", {})
        evidence_report = result.get("evidence", {})
        
        if not isinstance(ml_risk, dict): ml_risk = {}
        if not isinstance(decision_result, dict): decision_result = {}
        
        evidence_list = []
        if isinstance(evidence_report, dict):
            evidences = evidence_report.get("evidences", [])
            for ev in evidences:
                if isinstance(ev, dict): evidence_list.append(ev)
                else: evidence_list.append(ev.model_dump())
        elif hasattr(evidence_report, "evidences"):
            for ev in evidence_report.evidences:
                evidence_list.append(ev.model_dump())
                
        risk_evaluation = {
            "risk_score": ml_risk.get("risk_score", 0.0),
            "risk_level": ml_risk.get("risk_level", "Unknown"),
            "confidence": ml_risk.get("confidence", 0.0),
            "recommended_action": decision_result.get("final_decision", "Proceed"),
            "scam_type": scam_type,
            "reasoning": [
                rule_reason,
                decision_result.get("decision_reason", "")
            ],
            "evidence": evidence_list
        }
        
        risk_event = risk_event_repo.create(db, obj_in={
            "transaction_id": transaction.id,
            "risk_score": risk_evaluation["risk_score"],
            "risk_level": risk_evaluation["risk_level"],
            "confidence": risk_evaluation["confidence"],
            "recommended_action": risk_evaluation["recommended_action"],
            "reason_codes": risk_evaluation["reasoning"],  # Save plain-language reasoning to DB
            "features": {
                "scam_type": scam_type,
                "rule_reason": rule_reason
            }
        })
        db.commit()
        
        # 6. PENDING_DECISION
        TransactionOrchestrator._update_state(db, transaction, TransactionState.PENDING_DECISION)
        
        decision = decision_result.get("final_decision", "APPROVE_TRANSACTION")
        if decision == "APPROVE_TRANSACTION":
            TransactionOrchestrator._update_state(db, transaction, TransactionState.APPROVED)
            TransactionOrchestrator._update_state(db, transaction, TransactionState.STEP_UP_AUTHENTICATION)
            message = decision_result.get("decision_reason", "Transfer Approved. Awaiting Authentication.")
        elif decision in ["REQUEST_MORE_INFORMATION", "ESCALATE_TO_HUMAN"]:
            TransactionOrchestrator._update_state(db, transaction, TransactionState.AWAITING_CUSTOMER_RESPONSE)
            message = decision_result.get("decision_reason", "Transfer requires conversation and verification")
        else:
            TransactionOrchestrator._update_state(db, transaction, TransactionState.BLOCKED)
            message = decision_result.get("decision_reason", "Transfer Rejected due to High Risk")
            
        return TransferDecisionResponse(
            transaction=TransactionResponse.model_validate(transaction),
            risk_evaluation=risk_evaluation,
            message=message
        )

    @staticmethod
    def authenticate_and_execute(db: Session, transaction_id: int, user_id: int) -> TransactionResponse:
        transaction = transaction_repo.get(db, id=transaction_id)
        if not transaction or transaction.account.user_id != user_id:
            raise NotFoundException("Transaction not found")
            
        if transaction.status not in [TransactionState.STEP_UP_AUTHENTICATION]:
            raise BadRequestException(f"Transaction cannot be executed from state {transaction.status}")
            
        TransactionOrchestrator._update_state(db, transaction, TransactionState.EXECUTING)
        
        # In a real system, verify auth token or MPIN here.
        # We assume the API endpoint handled that validation.
        
        sender_account = transaction.account
        if sender_account.balance < transaction.amount:
            TransactionOrchestrator._update_state(db, transaction, TransactionState.FAILED)
            raise BadRequestException("Insufficient balance during execution")
            
        sender_account.balance -= transaction.amount
        
        # Here we could also log audit events, send notifications
        logger.info(f"Ledger updated for transaction {transaction_id}. Balance deducted.")
        
        # Dynamically update the user's BehaviorProfile / Digital Twin
        try:
            from backend.app.models.behavior_profile import BehaviorProfile
            from backend.app.models.user import User
            
            user = db.query(User).filter(User.id == user_id).first()
            profile = db.query(BehaviorProfile).filter(BehaviorProfile.user_id == user_id).first()
            if not profile:
                profile = BehaviorProfile(user_id=user_id)
                db.add(profile)
                db.flush()
                
            # 1. Update stats
            profile.transaction_count = (profile.transaction_count or 0) + 1
            count = profile.transaction_count
            
            # Recalculate average transaction amount
            prev_avg = profile.avg_transaction_amount or 0.0
            profile.avg_transaction_amount = ((prev_avg * (count - 1)) + transaction.amount) / count
            
            # Recalculate average daily spending
            now = datetime.utcnow()
            days_registered = max(1, (now - user.created_at.replace(tzinfo=None)).days) if user.created_at else 1
            profile.average_daily_transactions = count / float(days_registered)
            
            # Update temporal context
            profile.preferred_transfer_hour = int(now.hour)
            profile.last_transaction = now
            profile.average_balance = float(sender_account.balance)
            
            # Add to trusted recipients list if not already present
            if transaction.recipient_id:
                current_recipients = list(profile.trusted_recipients or [])
                if transaction.recipient_id not in current_recipients:
                    current_recipients.append(transaction.recipient_id)
                    profile.trusted_recipients = current_recipients
            
            # 2. Update AI Trust Timeline & Score based on transaction count
            if count <= 5:
                profile.trust_level = "NEW"
                profile.trust_score = int(50 + (count * 3))
            elif count <= 20:
                profile.trust_level = "LEARNING"
                profile.trust_score = int(65 + ((count - 5) * 0.8))
            elif count <= 100:
                profile.trust_level = "ESTABLISHED"
                profile.trust_score = int(77 + ((count - 20) * 0.2))
            else:
                profile.trust_level = "TRUSTED"
                profile.trust_score = min(99, int(93 + ((count - 100) * 0.05)))
                
            logger.info(f"Updated BehaviorProfile for user {user_id}. Count: {count}, Trust Level: {profile.trust_level}, Trust Score: {profile.trust_score}")
        except Exception as profile_err:
            logger.error(f"Failed to update BehaviorProfile on transaction completion: {profile_err}")
        
        db.commit()
        
        TransactionOrchestrator._update_state(db, transaction, TransactionState.COMPLETED)
        
        return TransactionResponse.model_validate(transaction)
