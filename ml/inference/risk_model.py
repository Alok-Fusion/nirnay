"""
Inference Engine Module
Wraps the ML pipeline to provide a clean prediction API for downstream services (LangGraph/Backend).
"""
import pandas as pd
import numpy as np
from typing import Dict, Any
from ml.registry.model_registry import ModelRegistry
from ml.explainability.shap_explainer import SHAPExplainer

class RiskInferenceEngine:
    def __init__(self):
        print("Loading latest model from registry...")
        self.model, self.preprocessor, self.fe, self.meta = ModelRegistry.load_latest_model()
        
        # Determine feature names for SHAP
        cat_features = self.preprocessor.preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(self.preprocessor.categorical_cols)
        self.feature_names = self.preprocessor.numerical_cols + list(cat_features)
        
        # Initialize Explainer lazily
        self.explainer = None
        
    def _initialize_explainer(self, X_processed: pd.DataFrame):
        if self.explainer is None:
            # We initialize SHAP explainer with a dummy background since true background is stored in training
            self.explainer = SHAPExplainer(self.model, X_processed)

    def get_risk_level(self, score: float):
        if score <= 20: return "Very Low"
        elif score <= 40: return "Low"
        elif score <= 60: return "Medium"
        elif score <= 80: return "High"
        else: return "Critical"
        
    def get_recommended_action(self, risk_level: str):
        actions = {
            "Very Low": "Proceed",
            "Low": "Proceed",
            "Medium": "Explain",
            "High": "Start Conversation",
            "Critical": "Conversation + Strong Recommendation"
        }
        return actions.get(risk_level, "Unknown")

    def predict(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes raw transaction data (joined dict), processes it, and returns the risk evaluation.
        """
        # Convert dict to DataFrame
        df = pd.DataFrame([transaction_data])
        
        # 1. Feature Engineering
        df_fe = self.fe.transform(df)
        
        # We drop risk_label and transaction_id for prediction
        drop_cols = [c for c in ['risk_label', 'transaction_id'] if c in df_fe.columns]
        X = df_fe.drop(columns=drop_cols)
        
        # 2. Preprocessing
        X_processed = self.preprocessor.transform(X)
        
        # Initialize SHAP if needed
        self._initialize_explainer(X_processed)
        
        # 3. Predict
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X_processed)[0]
            risk_prob = probs[1]
        else:
            risk_prob = self.model.predict(X_processed)[0]
            
        risk_score = min(max(round(risk_prob * 100, 2), 0), 100)
        risk_level = self.get_risk_level(risk_score)
        action = self.get_recommended_action(risk_level)
        
        # 4. Explain
        explanation = self.explainer.explain_local_instance(X_processed)
        
        # Formatting output
        response = {
            "transaction_id": transaction_data.get("transaction_id", "UNKNOWN"),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "confidence": round(abs(0.5 - risk_prob) * 200, 2), # % confidence away from decision boundary
            "recommended_action": action,
            "model_version": self.meta["version"],
            "explanation": explanation["top_factors"]
        }
        
        return response
