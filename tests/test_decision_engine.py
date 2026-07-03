import pytest
from ai.decision.engine import decision_engine
from ai.schemas.conversation import CustomerIntent

def test_decision_engine_customer_denial_overrides_low_risk():
    """
    Test that even if a transaction is low risk (0.0), a customer cancellation request
    immediately cancels the transaction without defaulting to approval.
    """
    state = {
        "context": {
            "ml_risk": {"risk_score": 10.0}
        },
        "policy_decision": {
            "requires_human_approval": False
        },
        "conversation_state": {
            "customer_intent": CustomerIntent.CANCEL_REQUESTED.value,
            "confirmation_attempts": 1,
            "contradiction_detected": False
        }
    }
    
    result = decision_engine(state)
    decision = result["decision_result"]["decision"]
    
    assert decision == "CANCEL_TRANSACTION", f"Expected CANCEL_TRANSACTION, got {decision}"

def test_decision_engine_high_risk_escalates_despite_authorization():
    """
    Test that if a customer authorizes a transaction but the risk score is > 90,
    the Risk Override Policy escalates the transaction.
    """
    state = {
        "context": {
            "ml_risk": {"risk_score": 95.0}
        },
        "policy_decision": {
            "requires_human_approval": False
        },
        "conversation_state": {
            "customer_intent": CustomerIntent.AUTHORIZED.value,
            "confirmation_attempts": 1,
            "contradiction_detected": False
        }
    }
    
    result = decision_engine(state)
    decision = result["decision_result"]["decision"]
    
    assert decision == "ESCALATE_TO_HUMAN", f"Expected ESCALATE_TO_HUMAN, got {decision}"

def test_decision_engine_missing_info_requests_more():
    """
    Test that if intent is uncertain, the engine requests more info.
    """
    state = {
        "context": {
            "ml_risk": {"risk_score": 50.0}
        },
        "policy_decision": {
            "requires_human_approval": False
        },
        "conversation_state": {
            "customer_intent": CustomerIntent.UNCERTAIN.value,
            "confirmation_attempts": 1,
            "contradiction_detected": False
        }
    }
    
    result = decision_engine(state)
    decision = result["decision_result"]["decision"]
    
    assert decision == "REQUEST_MORE_INFORMATION", f"Expected REQUEST_MORE_INFORMATION, got {decision}"
