"""
SHAP Explainability Module
Generates model explanations (Global and Local).
"""
import os
import shap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import warnings

# Suppress SHAP lightgbm warning
warnings.filterwarnings('ignore', message='.*LightGBM binary classifier with TreeExplainer shap values output has changed.*')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLOTS_DIR = os.path.join(BASE_DIR, "ml", "evaluation", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

class SHAPExplainer:
    def __init__(self, model, X_train: pd.DataFrame):
        self.model = model
        self.feature_names = X_train.columns.tolist()
        
        print("Initializing SHAP Explainer...")
        # Choose explainer based on model type
        model_type = type(model).__name__
        if model_type in ['RandomForestClassifier', 'XGBClassifier', 'LGBMClassifier']:
            # TreeExplainer is fast for tree-based models
            self.explainer = shap.TreeExplainer(model)
        else:
            # Fallback to KernelExplainer using a background summary
            background = shap.kmeans(X_train, 50)
            self.explainer = shap.KernelExplainer(model.predict_proba, background)
            
    def generate_global_explanations(self, X_sample: pd.DataFrame, max_display=20):
        print("Generating SHAP Global Explanations...")
        shap_values = self.explainer.shap_values(X_sample)
        
        # For some models/versions, shap_values is a list for classification [class 0, class 1]
        if isinstance(shap_values, list):
            shap_vals = shap_values[1]  # positive class
        else:
            shap_vals = shap_values
            
        # Summary Plot (Bar)
        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_vals, X_sample, plot_type="bar", show=False, max_display=max_display)
        plt.title("SHAP Global Feature Importance")
        bar_path = os.path.join(PLOTS_DIR, "shap_summary_bar.png")
        plt.savefig(bar_path, bbox_inches='tight')
        plt.close()
        
        # Summary Plot (Dot/Violin)
        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_vals, X_sample, show=False, max_display=max_display)
        plt.title("SHAP Feature Impact")
        dot_path = os.path.join(PLOTS_DIR, "shap_summary_dot.png")
        plt.savefig(dot_path, bbox_inches='tight')
        plt.close()
        
        return bar_path, dot_path
        
    def explain_local_instance(self, instance: pd.DataFrame):
        """
        Explains a single transaction. Returns top positive and negative contributing features.
        """
        shap_values = self.explainer.shap_values(instance)
        expected_value = self.explainer.expected_value
        
        if isinstance(shap_values, list):
            shap_vals = shap_values[1][0]
            exp_val = expected_value[1]
        else:
            shap_vals = shap_values[0]
            if isinstance(expected_value, (list, np.ndarray)):
                exp_val = expected_value[1] if len(expected_value)>1 else expected_value[0]
            else:
                exp_val = expected_value

        # Pair feature names with their SHAP values
        feature_contributions = list(zip(self.feature_names, shap_vals, instance.iloc[0].values))
        
        # Sort by absolute impact
        feature_contributions.sort(key=lambda x: abs(x[1]), reverse=True)
        
        contributions = []
        for name, shap_val, val in feature_contributions[:10]:
            if abs(shap_val) > 0.01: # threshold for significance
                contributions.append({
                    "feature": name,
                    "value": val,
                    "contribution": shap_val,
                    "impact": "Increases Risk" if shap_val > 0 else "Decreases Risk"
                })
                
        return {
            "base_value": exp_val,
            "top_factors": contributions
        }
