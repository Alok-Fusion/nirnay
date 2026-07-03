from typing import Dict, Any
from backend.app.services.ml_service import ml_service

import numpy as np

def _convert_numpy(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return _convert_numpy(obj.tolist())
    elif isinstance(obj, dict):
        return {k: _convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_numpy(i) for i in obj]
    return obj

def get_ml_risk_assessment(transaction_data: Dict[str, Any]) -> Dict[str, Any]:
    """Invokes the existing ML service to get the prediction and SHAP explanations."""
    # This wraps the existing backend service
    result = ml_service.analyze_transaction(transaction_data)
    
    # Normalize the output into the expected MLRiskResult format if needed
    features = transaction_data.copy()
    
    response = {
        "risk_score": result.get("risk_score", 0.0),
        "risk_level": result.get("risk_level", "Unknown"),
        "confidence": result.get("confidence", 0.0),
        "reason_codes": result.get("reason_codes", []),
        "features": features,
        "shap_values": result.get("explanation", None)
    }
    
    return _convert_numpy(response)
