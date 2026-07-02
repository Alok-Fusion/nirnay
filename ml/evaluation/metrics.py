"""
Evaluation Metrics Module
Calculates model performance metrics.
"""
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, confusion_matrix
)

class Evaluator:
    @staticmethod
    def get_metrics(y_true, y_pred, y_probs):
        return {
            "Accuracy": accuracy_score(y_true, y_pred),
            "Precision": precision_score(y_true, y_pred, zero_division=0),
            "Recall": recall_score(y_true, y_pred, zero_division=0),
            "F1_Score": f1_score(y_true, y_pred, zero_division=0),
            "ROC_AUC": roc_auc_score(y_true, y_probs)
        }
        
    @staticmethod
    def get_confusion_matrix(y_true, y_pred):
        cm = confusion_matrix(y_true, y_pred)
        return {
            "TN": int(cm[0, 0]),
            "FP": int(cm[0, 1]),
            "FN": int(cm[1, 0]),
            "TP": int(cm[1, 1])
        }
