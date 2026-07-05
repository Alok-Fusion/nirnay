import pytest
from backend.app.ai.decision.rule_engine import RuleEngine, SCAM_TYPE_NONE

def test_rule_engine_limit_exceeded():
    """
    Test that if daily limit is exceeded, RuleEngine returns SUSPICIOUS verdict
    with a clear warning reason.
    """
    features = {
        "limit_exceeded": 1.0,
        "daily_limit": 5000.0,
        "daily_spent_sum": 4500.0,
        "recipient_transfer_count": 5,
        "trusted_recipient": 1.0
    }
    
    verdict, reason, scam_type = RuleEngine.evaluate(features, 1000.0)
    
    assert verdict == "SUSPICIOUS"
    assert "daily transfer limit of $5,000" in reason
    assert "Spent today: $4,500.00" in reason
    assert scam_type == SCAM_TYPE_NONE

def test_rule_engine_limit_not_exceeded():
    """
    Test that standard safety checks apply when limit is not exceeded.
    """
    features = {
        "limit_exceeded": 0.0,
        "daily_limit": 5000.0,
        "daily_spent_sum": 0.0,
        "recipient_transfer_count": 5,
        "trusted_recipient": 1.0,
        "amount_ratio": 1.0,
        "night_transaction": 0.0,
        "transactions_last_hour": 0,
        "transactions_last_24h": 0
    }
    
    # Trusted recipient, amount 1000. should evaluate to SAFE
    verdict, reason, scam_type = RuleEngine.evaluate(features, 1000.0)
    assert verdict == "SAFE"
