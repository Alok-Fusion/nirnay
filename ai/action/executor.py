import logging
import uuid
from typing import Dict, Any
from ai.state.decision_state import DecisionState
from ai.schemas.decision import DecisionResult
from ai.observability.metrics import trace_agent

logger = logging.getLogger(__name__)

# --- Mock Banking Services ---
def process_transfer(transaction_id: str, amount: float):
    logger.info(f"🏦 BANK API: Processing transfer {transaction_id} for {amount}.")
    return True

def freeze_transaction(transaction_id: str):
    logger.info(f"🏦 BANK API: Freezing transaction {transaction_id}.")
    return True

def notify_customer(customer_id: int, message: str):
    logger.info(f"📱 NOTIFICATION API (User {customer_id}): {message}")
    return True

def create_case(transaction_id: str, risk_score: float, reason: str) -> str:
    case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"
    logger.info(f"⚖️ CASE MANAGEMENT API: Created Case {case_id} for Tx {transaction_id}. Risk: {risk_score}. Reason: {reason}")
    return case_id

# --- Action Executor ---
@trace_agent("ActionExecutor")
def action_executor(state: DecisionState) -> Dict[str, Any]:
    """
    Executes mock banking API calls based on the deterministic Decision Result.
    Generates a Case ID if escalated.
    """
    result_data = state.get("decision_result")
    if not result_data:
        raise ValueError("Missing decision_result in ActionExecutor.")
        
    result = DecisionResult(**result_data)
    transaction_id = state.get("transaction_id", "UNKNOWN")
    customer_id = state.get("raw_customer_id", 0)
    
    context_data = state.get("context", {})
    amount = context_data.get("transaction", {}).get("amount", 0.0)
    risk_score = context_data.get("ml_risk", {}).get("risk_score", 0.0)
    
    case_id = None
    
    if result.decision == "APPROVE_TRANSACTION":
        process_transfer(transaction_id, amount)
        notify_customer(customer_id, "Your transaction has been securely processed.")
        
    elif result.decision == "CANCEL_TRANSACTION":
        freeze_transaction(transaction_id)
        notify_customer(customer_id, "Your transaction was cancelled successfully as requested.")
        
    elif result.decision == "BLOCK_TRANSACTION":
        freeze_transaction(transaction_id)
        notify_customer(customer_id, "Your transaction was blocked by our security systems.")
        
    elif result.decision == "ESCALATE_TO_HUMAN":
        freeze_transaction(transaction_id)
        case_id = create_case(transaction_id, risk_score, result.reason)
        notify_customer(customer_id, f"Your transaction is under review by our fraud team. Ref: {case_id}")
        
    elif result.decision == "REQUEST_MORE_INFORMATION":
        # Action Executor shouldn't usually be called on non-terminal states, 
        # but if it is, we just let the graph route back.
        pass

    return {
        "case_id": case_id,
        "next_agent": "AuditLogger"
    }
