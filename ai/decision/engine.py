import logging
from typing import Dict, Any
from ai.state.decision_state import DecisionState
from ai.schemas.decision import DecisionResult
from ai.schemas.conversation import CustomerIntent
from ai.observability.metrics import trace_agent

logger = logging.getLogger(__name__)

@trace_agent("DecisionResolutionEngine")
def decision_engine(state: DecisionState) -> Dict[str, Any]:
    """
    Deterministic rule-based engine to make the final transaction decision.
    No LLM is used here.
    """
    context_data = state.get("context", {})
    policy_data = state.get("policy_decision", {})
    conversation_data = state.get("conversation_state", {})
    
    # Extract needed variables
    risk_score = context_data.get("ml_risk", {}).get("risk_score", 0.0)
    requires_human_approval = policy_data.get("requires_human_approval", False)
    
    intent_str = conversation_data.get("customer_intent", "UNKNOWN")
    try:
        intent = CustomerIntent(intent_str)
    except ValueError:
        intent = CustomerIntent.UNKNOWN
        
    attempts = conversation_data.get("confirmation_attempts", 0)
    contradiction = conversation_data.get("contradiction_detected", False)
    
    # Risk Override Policy
    # If the score is extremely high (> 90), or PolicyAgent explicitly requires human approval
    # we escalate even if the customer authorizes it, to protect against Account Takeover.
    risk_override = risk_score >= 90.0 or requires_human_approval

    decision = None
    reason = ""
    requires_escalation = False
    
    # Precedence Level 1: Customer Authorization
    if intent == CustomerIntent.CANCEL_REQUESTED:
        decision = "CANCEL_TRANSACTION"
        reason = "Customer explicitly requested cancellation. This overrides all other rules."
        
    elif contradiction and attempts < 2:
        decision = "REQUEST_MORE_INFORMATION"
        reason = "Contradiction detected in customer input. Seeking clarification."
        
    elif attempts >= 2 and intent not in [CustomerIntent.AUTHORIZED, CustomerIntent.CANCEL_REQUESTED]:
        decision = "ESCALATE_TO_HUMAN"
        reason = "Maximum confirmation attempts reached without clear intent."
        requires_escalation = True
        
    elif intent in [CustomerIntent.CONFUSED, CustomerIntent.UNCERTAIN, CustomerIntent.UNKNOWN] and attempts > 0:
        decision = "REQUEST_MORE_INFORMATION"
        reason = "Customer intent unclear. Requesting more information."
        
    # Precedence Level 2 & 3: Fraud Risk & Policy Rules
    elif intent == CustomerIntent.AUTHORIZED or attempts == 0: 
        # If authorized, OR if we haven't asked yet (straight-through processing attempt)
        if risk_override:
            decision = "ESCALATE_TO_HUMAN"
            reason = "Risk Override Policy triggered (extreme risk or policy block)."
            requires_escalation = True
        elif requires_human_approval and attempts == 0:
            # We need to ask the customer
            decision = "REQUEST_MORE_INFORMATION"
            reason = "Policy requires human confirmation."
        else:
            decision = "APPROVE_TRANSACTION"
            reason = "Customer authorized and risk is acceptable, or low risk straight-through."
            
    # Fallback
    if not decision:
        decision = "ESCALATE_TO_HUMAN"
        reason = "Fallback decision due to unhandled state."
        requires_escalation = True

    result = DecisionResult(
        decision=decision,
        reason=reason,
        confidence=1.0, # Deterministic logic is always 100% confident
        recommended_actions=policy_data.get("recommendations", []),
        workflow_completed=decision in ["APPROVE_TRANSACTION", "BLOCK_TRANSACTION", "CANCEL_TRANSACTION", "ESCALATE_TO_HUMAN"],
        requires_human_escalation=requires_escalation
    )

    return {
        "decision_result": result.model_dump(),
        "workflow_status": "COMPLETED" if result.workflow_completed else "RUNNING",
        "next_agent": "ActionExecutor" if result.workflow_completed else "ConversationOrchestrator"
    }
