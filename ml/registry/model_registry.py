"""
Model Registry Module
Handles saving and loading of models, pipelines, and metadata.
"""
import os
import joblib
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "ml", "models")
os.makedirs(MODELS_DIR, exist_ok=True)

class ModelRegistry:
    @staticmethod
    def save_model_artifacts(model, preprocessor, feature_engineer, metrics, model_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        version = f"{model_name}_{timestamp}"
        
        # Paths
        model_path = os.path.join(MODELS_DIR, f"{version}_model.joblib")
        prep_path = os.path.join(MODELS_DIR, f"{version}_preprocessor.joblib")
        fe_path = os.path.join(MODELS_DIR, f"{version}_fe.joblib")
        meta_path = os.path.join(MODELS_DIR, f"{version}_metadata.json")
        
        # Save artifacts
        joblib.dump(model, model_path)
        joblib.dump(preprocessor, prep_path)
        joblib.dump(feature_engineer, fe_path)
        
        # Save metadata
        metadata = {
            "version": version,
            "model_type": model_name,
            "training_date": datetime.now().isoformat(),
            "metrics": metrics,
            "artifacts": {
                "model": model_path,
                "preprocessor": prep_path,
                "feature_engineer": fe_path
            }
        }
        
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)
            
        print(f"Successfully saved {model_name} artifacts to ml/models/ (Version: {version})")
        
        # Save a 'latest' pointer
        pointer_path = os.path.join(MODELS_DIR, "latest.json")
        with open(pointer_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)
            
        return metadata

    @staticmethod
    def load_latest_model():
        pointer_path = os.path.join(MODELS_DIR, "latest.json")
        if not os.path.exists(pointer_path):
            raise FileNotFoundError("No 'latest.json' found in registry.")
            
        with open(pointer_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            
        model = joblib.load(meta["artifacts"]["model"])
        preprocessor = joblib.load(meta["artifacts"]["preprocessor"])
        fe = joblib.load(meta["artifacts"]["feature_engineer"])
        
        return model, preprocessor, fe, meta
