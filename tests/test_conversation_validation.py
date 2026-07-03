import pytest
from unittest.mock import patch, MagicMock
from ai.schemas.conversation import ConversationAction, ConversationState, CustomerIntent
from langchain_core.messages import SystemMessage, HumanMessage

class MockValidationError(Exception):
    pass

@patch('ai.conversation.agent.llm_factory')
def test_conversation_agent_validation_retry(mock_llm_factory):
    """
    Test that the conversation agent catches validation errors and retries.
    """
    # Setup mock LLM
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    mock_llm.with_structured_output.return_value = mock_structured_llm
    mock_llm_factory.get_llm.return_value = mock_llm
    
    # Configure structured LLM to fail on first call, succeed on second call
    valid_action = ConversationAction(
        action_type="AskQuestion",
        message_to_customer="Is this correct?",
        requires_response=True,
        updated_state=ConversationState(customer_intent=CustomerIntent.UNKNOWN)
    )
    
    mock_structured_llm.invoke.side_effect = [
        MockValidationError("Input should be a valid boolean, unable to interpret input"), 
        valid_action
    ]
    
    from ai.conversation.agent import conversation_agent
    
    state = {
        "evidence": {
            "transaction_id": "TX-123",
            "overall_summary": "Test evidence",
            "primary_risk_factors": [],
            "mitigating_factors": []
        },
        "policy_decision": {"is_compliant": True, "action": "Require Customer Confirmation", "requires_human_approval": False, "rationale": "test", "recommendations": []},
        "context": {
            "customer": {"user_id": "1", "name": "Test", "email": "test@test.com", "full_name": "Test User", "role": "user"},
            "transaction": {"transaction_id": "TX-123", "currency": "USD", "amount": 100.0, "type": "TRANSFER", "timestamp": "2026-07-02"},
            "recipient": {"name": "Test", "account_number_masked": "****", "bank_code": "000", "is_trusted": False},
            "behavior": {"is_new_device": False, "is_new_location": False, "velocity_1h": 1, "velocity_24h": 1, "avg_transaction_amount": 50.0, "frequent_categories": [], "last_updated": "2026-07-02"},
            "ml_risk": {"risk_score": 10.0, "risk_level": "LOW", "confidence": 0.9, "reason_codes": [], "features": {}}
        },
        "messages": []
    }
    
    result = conversation_agent(state)
    
    # Assert that invoke was called twice (initial + 1 retry)
    assert mock_structured_llm.invoke.call_count == 2
    
    # Assert that the second call contained the correction prompt
    second_call_messages = mock_structured_llm.invoke.call_args_list[1][0][0]
    last_msg = second_call_messages[-1]
    
    assert isinstance(last_msg, HumanMessage)
    assert "Your previous response failed schema validation" in last_msg.content
    
    # Assert successful fallback result
    assert result["last_action"]["action_type"] == "AskQuestion"
    assert result["workflow_status"] == "AWAITING_CUSTOMER"
