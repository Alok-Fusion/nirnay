"""
Master Training Script
Executes the entire Machine Learning pipeline.
"""
import os
import sys
# Add project root to python path so ml.* imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sklearn.model_selection import train_test_split
from ml.data.joiner import DataJoiner
from ml.feature_engineering.pipeline import FeatureEngineer
from ml.preprocessing.pipeline import Preprocessor
from ml.training.trainer import ModelTrainer
from ml.evaluation.metrics import Evaluator
from ml.evaluation.plots import Plotter
from ml.explainability.shap_explainer import SHAPExplainer
from ml.registry.model_registry import ModelRegistry

def main():
    print("="*60)
    print("NIRNAY - Machine Learning Pipeline Execution")
    print("="*60)
    
    # 1. Load and Join Data
    joiner = DataJoiner()
    df = joiner.create_master_dataset()
    
    # 2. Feature Engineering
    fe = FeatureEngineer()
    df_features = fe.fit_transform(df)
    
    # Define Target and Features
    y = df_features['risk_label']
    X = df_features.drop(columns=['risk_label', 'transaction_id'], errors='ignore')
    
    print(f"Target distribution:\n{y.value_counts()}")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")
    
    # 3. Preprocessing
    print("\nApplying Preprocessing...")
    preprocessor = Preprocessor()
    X_train_processed = preprocessor.fit_transform(X_train, y_train)
    X_test_processed = preprocessor.transform(X_test)
    
    # 4. Model Training & Selection
    trainer = ModelTrainer(random_state=42)
    # Split train again for validation during selection
    X_t, X_v, y_t, y_v = train_test_split(X_train_processed, y_train, test_size=0.1, random_state=42, stratify=y_train)
    
    results, best_name, best_model = trainer.train_and_evaluate(X_t, y_t, X_v, y_v)
    
    # 5. Hyperparameter Tuning
    best_model = trainer.optimize_best_model(X_train_processed, y_train)
    
    # 6. Final Evaluation
    print("\nEvaluating Final Model on Test Set...")
    preds = best_model.predict(X_test_processed)
    probs = best_model.predict_proba(X_test_processed)[:, 1] if hasattr(best_model, "predict_proba") else preds
    
    metrics = Evaluator.get_metrics(y_test, preds, probs)
    print("Final Test Metrics:")
    for k, v in metrics.items():
        print(f"  {k}: {v:.4f}")
        
    # Generate Plots
    print("\nGenerating Evaluation Plots...")
    Plotter.plot_roc_curve(y_test, probs, model_name=best_name)
    Plotter.plot_pr_curve(y_test, probs, model_name=best_name)
    Plotter.plot_confusion_matrix(y_test, preds, model_name=best_name)
    Plotter.plot_calibration_curve(y_test, probs, model_name=best_name)
    
    if hasattr(best_model, "feature_importances_"):
        Plotter.plot_feature_importance(best_model.feature_importances_, X_train_processed.columns)
        
    # 7. Explainability (SHAP)
    # We use a background summary for SHAP to avoid massive runtime overhead during global explanations
    explainer = SHAPExplainer(best_model, X_train_processed.sample(100, random_state=42))
    # Generate global summary on a sample of test data
    explainer.generate_global_explanations(X_test_processed.sample(200, random_state=42), max_display=15)
    
    # 8. Registry Save
    ModelRegistry.save_model_artifacts(
        model=best_model, 
        preprocessor=preprocessor, 
        feature_engineer=fe, 
        metrics=metrics, 
        model_name=best_name
    )
    
    print("\nPipeline execution completed successfully.")

if __name__ == "__main__":
    main()
