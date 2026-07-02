import logging
import sys
import os

# Append the root path so that we can import ml.inference
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if root_path not in sys.path:
    sys.path.append(root_path)

from typing import Dict, Any

logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        self.engine = None
        try:
            from ml.inference.risk_model import RiskInferenceEngine
            self.engine = RiskInferenceEngine()
            logger.info("RiskInferenceEngine loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load RiskInferenceEngine: {e}")
            
    def analyze_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.engine:
            logger.warning("ML Engine not loaded. Returning default low risk.")
            return {
                "transaction_id": transaction_data.get("transaction_id", "UNKNOWN"),
                "risk_score": 0.0,
                "risk_level": "Very Low",
                "confidence": 100.0,
                "recommended_action": "Proceed",
                "model_version": "dummy",
                "explanation": {}
            }
        try:
            result = self.engine.predict(transaction_data)
            return result
        except Exception as e:
            logger.error(f"ML prediction failed: {e}", exc_info=True)
            # Fail open or fail closed? For a bank, fail safe (High Risk) or fallback to manual review
            return {
                "transaction_id": transaction_data.get("transaction_id", "UNKNOWN"),
                "risk_score": 100.0,
                "risk_level": "Critical",
                "confidence": 0.0,
                "recommended_action": "Error - Manual Review Required",
                "reason_codes": ["ML_ERROR"]
            }

ml_service = MLService()
