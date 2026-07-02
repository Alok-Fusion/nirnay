"""
Evaluation Plots Module
Generates and saves visual evaluation artifacts.
"""
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    roc_curve, auc, precision_recall_curve, ConfusionMatrixDisplay
)
from sklearn.calibration import calibration_curve

# Ensure the plots directory exists
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLOTS_DIR = os.path.join(BASE_DIR, "ml", "evaluation", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

class Plotter:
    @staticmethod
    def plot_roc_curve(y_true, y_probs, model_name="Best Model"):
        fpr, tpr, _ = roc_curve(y_true, y_probs)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.3f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'Receiver Operating Characteristic - {model_name}')
        plt.legend(loc="lower right")
        
        filepath = os.path.join(PLOTS_DIR, "roc_curve.png")
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
        return filepath

    @staticmethod
    def plot_pr_curve(y_true, y_probs, model_name="Best Model"):
        precision, recall, _ = precision_recall_curve(y_true, y_probs)
        
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, color='blue', lw=2)
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title(f'Precision-Recall Curve - {model_name}')
        
        filepath = os.path.join(PLOTS_DIR, "pr_curve.png")
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
        return filepath

    @staticmethod
    def plot_confusion_matrix(y_true, y_pred, model_name="Best Model"):
        plt.figure(figsize=(6, 5))
        ConfusionMatrixDisplay.from_predictions(y_true, y_pred, cmap="Blues", colorbar=False)
        plt.title(f'Confusion Matrix - {model_name}')
        
        filepath = os.path.join(PLOTS_DIR, "confusion_matrix.png")
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
        return filepath

    @staticmethod
    def plot_calibration_curve(y_true, y_probs, model_name="Best Model"):
        prob_true, prob_pred = calibration_curve(y_true, y_probs, n_bins=10)
        
        plt.figure(figsize=(8, 6))
        plt.plot(prob_pred, prob_true, marker='o', linewidth=2, label=model_name)
        plt.plot([0, 1], [0, 1], linestyle='--', color='black', label='Perfectly calibrated')
        plt.xlabel('Mean predicted probability')
        plt.ylabel('Fraction of positives')
        plt.title('Calibration Curve')
        plt.legend()
        
        filepath = os.path.join(PLOTS_DIR, "calibration_curve.png")
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
        return filepath
        
    @staticmethod
    def plot_feature_importance(importances, feature_names, top_n=20):
        # Sort features
        indices = importances.argsort()[-top_n:]
        sorted_features = [feature_names[i] for i in indices]
        sorted_importances = importances[indices]
        
        plt.figure(figsize=(10, 8))
        plt.barh(sorted_features, sorted_importances, color='teal')
        plt.xlabel("Feature Importance")
        plt.title(f"Top {top_n} Features")
        
        filepath = os.path.join(PLOTS_DIR, "feature_importance.png")
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
        return filepath
