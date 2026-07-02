"""
Scenario Tester
Runs the inference engine against all demo JSON scenarios generated in Phase 1.
"""
import os
import json
from ml.inference.risk_model import RiskInferenceEngine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEMO_DIR = os.path.join(BASE_DIR, "datasets", "demo")

def test_scenarios():
    print("Initializing Risk Inference Engine...")
    engine = RiskInferenceEngine()
    
    scenarios = [f for f in os.listdir(DEMO_DIR) if f.endswith(".json") and f != "_index.json"]
    print(f"Found {len(scenarios)} scenarios to test.\n")
    
    for scenario_file in scenarios:
        path = os.path.join(DEMO_DIR, scenario_file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print(f"--- Testing Scenario: {scenario_file} ---")
        
        # In reality, backend sends a flattened transaction dictionary
        # We simulate that flattening here
        flat_txn = data.get("transaction", {}).copy()
        
        if "transaction_type" not in flat_txn:
            flat_txn["transaction_type"] = "Debit"
        
        # provide defaults for missing fields needed by FE
        if "timestamp" not in flat_txn:
            from datetime import datetime
            flat_txn["timestamp"] = datetime(2026, 7, 2, 14, 0).isoformat()
        
        # Bring in customer & account info for feature engineering
        cust = data.get("customer", {})
        beh = data.get("behavior", {})
        acct = data.get("account", {})
        
        flat_txn["customer_id"] = cust.get("customer_id", "DEMO-001")
        flat_txn["device_type_x"] = cust.get("device_type", "Mobile")
        flat_txn["usual_device"] = beh.get("usual_device", "Mobile")
        flat_txn["city"] = cust.get("city", "Mumbai")
        flat_txn["usual_location"] = beh.get("usual_location", "Mumbai")
        flat_txn["risk_profile"] = cust.get("risk_profile", "Medium")
        flat_txn["favorite_categories"] = beh.get("favorite_categories", "Transfer")
        flat_txn["digital_payment_ratio"] = beh.get("digital_payment_ratio", 0.8)
        
        flat_txn["current_balance"] = acct.get("current_balance", 50000)
        
        # recipient info
        flat_txn["trusted_recipient"] = False
        flat_txn["transaction_count"] = 0
        if data.get("recipient"):
            flat_txn["trusted_recipient"] = data["recipient"].get("trusted_recipient", False)
            flat_txn["transaction_count"] = data["recipient"].get("transaction_count", 0)
            
        # merchant info
        flat_txn["trust_score"] = 50
        flat_txn["reported_scam_count_rep"] = 0
        if data.get("merchant"):
            flat_txn["trust_score"] = data["merchant"].get("trust_score", 50)
            flat_txn["reported_scam_count_rep"] = data["merchant"].get("reported_scam_count", 0)
        
        # Add behavior profile aggregations
        flat_txn["average_transaction"] = cust.get("average_transaction", 2000)
        
        # Predict
        try:
            result = engine.predict(flat_txn)
            print(f"Risk Score: {result['risk_score']} ({result['risk_level']})")
            print(f"Action: {result['recommended_action']}")
            print("Top Factors:")
            for f in result['explanation'][:3]:
                print(f"  - {f['feature']}: {f['impact']} (Val: {f['value']})")
        except Exception as e:
            print(f"Error predicting {scenario_file}: {e}")
            
        print("\n")

if __name__ == "__main__":
    test_scenarios()
