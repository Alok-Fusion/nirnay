from backend.app.services.ml_service import ml_service

def test_ml_service_predict_dummy():
    # If the real ML engine fails to load or we pass mock data,
    # the fallback returns a Critical risk event.
    data = {"transaction_id": "tx_123", "amount": 500}
    # For unit tests without ML model loaded, we expect it might return fallback
    result = ml_service.analyze_transaction(data)
    assert result is not None
    assert "risk_score" in result
    assert "transaction_id" in result
    assert result["transaction_id"] == "tx_123"
