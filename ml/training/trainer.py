"""
Model Trainer Module
Handles training, hyperparameter tuning, and model selection.
"""
import time
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from sklearn.metrics import roc_auc_score, f1_score

try:
    import xgboost as xgb
except ImportError:
    xgb = None

try:
    import lightgbm as lgb
except ImportError:
    lgb = None

class ModelTrainer:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.models = self._initialize_models()
        self.best_model_name = None
        self.best_model = None
        self.best_score = 0.0
        
    def _initialize_models(self):
        models = {
            "LogisticRegression": LogisticRegression(
                random_state=self.random_state, max_iter=1000, class_weight="balanced"
            ),
            "RandomForest": RandomForestClassifier(
                random_state=self.random_state, n_estimators=100, class_weight="balanced", n_jobs=-1
            )
        }
        
        if xgb is not None:
            models["XGBoost"] = xgb.XGBClassifier(
                random_state=self.random_state, 
                eval_metric="auc", 
                scale_pos_weight=10, # roughly based on 95/5 imbalance
                use_label_encoder=False,
                n_jobs=-1
            )
            
        if lgb is not None:
            models["LightGBM"] = lgb.LGBMClassifier(
                random_state=self.random_state,
                class_weight="balanced",
                n_jobs=-1
            )
            
        return models

    def train_and_evaluate(self, X_train, y_train, X_val, y_val):
        """
        Trains all models on the training set and evaluates on the validation set.
        Selects the best model based on ROC AUC.
        """
        results = {}
        print("Training models...")
        
        for name, model in self.models.items():
            print(f"  Training {name}...")
            start_time = time.time()
            model.fit(X_train, y_train)
            train_time = time.time() - start_time
            
            # Predict
            preds = model.predict(X_val)
            probs = model.predict_proba(X_val)[:, 1] if hasattr(model, "predict_proba") else preds
            
            # Evaluate
            auc = roc_auc_score(y_val, probs)
            f1 = f1_score(y_val, preds)
            
            results[name] = {
                "model": model,
                "val_auc": auc,
                "val_f1": f1,
                "train_time": train_time
            }
            
            print(f"    - AUC: {auc:.4f} | F1: {f1:.4f} | Time: {train_time:.2f}s")
            
            # Update best model
            if auc > self.best_score:
                self.best_score = auc
                self.best_model_name = name
                self.best_model = model
                
        print(f"\nBest model selected: {self.best_model_name} (AUC: {self.best_score:.4f})")
        return results, self.best_model_name, self.best_model

    def optimize_best_model(self, X_train, y_train):
        """
        Performs RandomizedSearchCV on the selected best model.
        """
        if self.best_model_name == "XGBoost":
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.05, 0.1],
                'subsample': [0.8, 1.0],
                'colsample_bytree': [0.8, 1.0]
            }
        elif self.best_model_name == "RandomForest":
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [None, 10, 20],
                'min_samples_split': [2, 5]
            }
        elif self.best_model_name == "LightGBM":
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [-1, 5, 10],
                'learning_rate': [0.01, 0.05, 0.1]
            }
        else:
            # Logistic Regression or others
            print(f"Skipping hyperparameter tuning for {self.best_model_name}")
            return self.best_model

        print(f"Optimizing {self.best_model_name}...")
        cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=self.random_state)
        
        search = RandomizedSearchCV(
            self.best_model, 
            param_distributions=param_grid,
            n_iter=10, 
            scoring='roc_auc', 
            cv=cv, 
            verbose=1, 
            random_state=self.random_state,
            n_jobs=-1
        )
        
        search.fit(X_train, y_train)
        print(f"Best parameters found: {search.best_params_}")
        print(f"Best CV AUC: {search.best_score_:.4f}")
        
        self.best_model = search.best_estimator_
        return self.best_model
