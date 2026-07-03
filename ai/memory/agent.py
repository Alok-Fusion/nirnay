import logging
from typing import Dict, Any
from ai.state.decision_state import DecisionState
from ai.tools.memory_tools import add_to_memory, search_memory
from ai.observability.metrics import trace_agent

logger = logging.getLogger(__name__)

@trace_agent("MemoryAgent")
def memory_agent(state: DecisionState) -> Dict[str, Any]:
    """
    Updates Long-term and Short-term memory with the outcome of this transaction.
    """
    context_data = state.get("context")
    policy_data = state.get("policy_decision")
    conversation_msgs = state.get("messages", [])
    
    from ai.schemas.context import DecisionContext
    from ai.schemas.policy import PolicyDecision
    
    context = DecisionContext(**context_data) if context_data else None
    policy = PolicyDecision(**policy_data) if policy_data else None
    
    if context and policy:
        action_taken = state.get("last_action", {}).get("action_type", policy.action) if state.get("last_action") else policy.action
        
        # Parse customer decision from conversation history
        customer_decision = "No response"
        if conversation_msgs and len(conversation_msgs) > 0:
            last_msg = conversation_msgs[-1]
            if last_msg.get('role') == 'user':
                customer_decision = last_msg.get('content')
                
        # Create a textual representation of the outcome
        recipient_name = context.recipient.name if context.recipient else "Unknown"
        is_trusted = context.recipient.is_trusted if context.recipient else False
        
        memory_text = (
            f"Transaction ID: {context.transaction.transaction_id}. "
            f"User ID: {context.customer.user_id}. "
            f"Recipient: {recipient_name} (Trusted: {is_trusted}). "
            f"Risk Score: {context.ml_risk.risk_score}. "
            f"Initial Policy: {policy.action}. "
            f"Customer Decision: {customer_decision}. "
            f"Final Action: {action_taken}."
        )
            
        metadata = {
            "user_id": context.customer.user_id,
            "transaction_id": context.transaction.transaction_id,
            "action": action_taken,
            "trusted_recipient": is_trusted,
            "customer_decision": customer_decision
        }
        
        # Save to FAISS
        add_to_memory(memory_text, metadata)
        logger.info("Detailed Memory saved to FAISS vector store.")
    
    return {
        "memory_context": {"updated": True},
        "next_agent": "END",
        "workflow_status": "COMPLETED"
    }
