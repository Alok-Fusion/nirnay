import logging
from typing import Dict, Any
from ai.state.decision_state import DecisionState
from ai.schemas.context import DecisionContext, CustomerProfile, TransactionContext, BehaviorProfile, RecipientInfo
from ai.tools.db_tools import get_customer_profile, get_behavior_profile, get_recipient_info
from ai.tools.ml_tools import get_ml_risk_assessment
from ai.tools.memory_tools import search_memory
from ai.observability.metrics import trace_agent

logger = logging.getLogger(__name__)

@trace_agent("ContextIntelligenceAgent")
def context_agent(state: DecisionState) -> Dict[str, Any]:
    """
    Collects customer information, transaction context, behavior profile,
    recipient information, and ML risk scores.
    Normalizes data and creates a complete Decision Context.
    """
    tx_id = state.get("transaction_id")
    raw_tx = state.get("raw_transaction_data")
    user_id = state.get("raw_customer_id")
    existing_context = state.get("context")
    
    if existing_context:
        # Idempotency: skip feature gathering if already present
        return {
            "next_agent": "RiskInterpretationAgent",
            "workflow_status": "RUNNING"
        }

    if not raw_tx:
        raw_tx = {}
    
    # 1. Fetch DB Context
    customer_data = get_customer_profile(user_id)
    behavior_data = get_behavior_profile(user_id)
    recipient_data = None
    if "recipient_id" in raw_tx and raw_tx["recipient_id"]:
        recipient_data = get_recipient_info(raw_tx["recipient_id"])
        
    # 2. Fetch ML Context
    ml_risk = get_ml_risk_assessment(raw_tx)
    
    # 3. Assemble DecisionContext
    customer = CustomerProfile(**customer_data) if customer_data else CustomerProfile(user_id=user_id, email="unknown", full_name="Unknown", role="CUSTOMER")
    behavior = BehaviorProfile(**behavior_data)
    transaction = TransactionContext(
        transaction_id=raw_tx.get("transaction_id", "unknown"),
        amount=raw_tx.get("amount", 0.0),
        currency=raw_tx.get("currency", "USD"),
        type=raw_tx.get("type", "TRANSFER")
    )
    
    recipient = RecipientInfo(**recipient_data) if recipient_data else None
    
    # Determine if recipient is new (mock logic for MVP: if recipient not found in trusted DB, it's new)
    if recipient:
        recipient.is_new = not recipient.is_trusted
    else:
        # If paying to an account number directly not saved
        recipient = RecipientInfo(
            account_number_masked="***" + str(raw_tx.get("account_number", ""))[-4:],
            bank_code=raw_tx.get("bank_code", "UNKNOWN"),
            name=raw_tx.get("recipient_name", "Unknown"),
            is_trusted=False,
            is_new=True
        )

    # 4. Fetch Memory Context
    try:
        past_memories = search_memory(f"Transactions for user {user_id}", k=3)
        past_interactions = [doc.get("content", str(doc)) for doc in past_memories] if past_memories else []
    except Exception as e:
        logger.warning(f"Failed to fetch FAISS memory: {e}")
        past_interactions = []

    decision_context = DecisionContext(
        customer=customer,
        transaction=transaction,
        behavior=behavior,
        recipient=recipient,
        merchant=None,
        ml_risk=ml_risk,
        historical_context={"past_memories": past_interactions}
    )
    
    return {
        "context": decision_context.model_dump(),
        "next_agent": "RiskInterpretationAgent",
        "workflow_status": "RUNNING"
    }
