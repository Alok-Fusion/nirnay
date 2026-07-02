# Model Training & Retraining Guide

This guide details how to execute, monitor, and extend the NIRNAY ML Pipeline.

## Executing the Pipeline

The master training script automates data joining, feature engineering, preprocessing, training, hyperparameter tuning, evaluation, explainability, and artifact registration.

```bash
# Ensure virtual environment is activated and dependencies are installed
pip install -r requirements.txt

# Run the master training pipeline
python ml/train.py
```

### Pipeline Steps
1. **Data Joining**: Loads all CSVs from `datasets/` and joins them into a master DataFrame of 50,000 records.
2. **Feature Engineering**: Applies `ml.feature_engineering.pipeline` to generate derived features.
3. **Preprocessing**: Fits the `ColumnTransformer` to scale numericals and one-hot encode categoricals.
4. **Model Selection**: Trains Logistic Regression, Random Forest, XGBoost, and LightGBM on a validation split. Selects the model with the highest ROC-AUC.
5. **Hyperparameter Tuning**: Performs `RandomizedSearchCV` on the selected best model with 3 Stratified K-Folds.
6. **Evaluation**: Generates predictions on the 20% holdout test set. Saves `roc_curve.png`, `pr_curve.png`, `confusion_matrix.png`, and `feature_importance.png` to `ml/evaluation/plots/`.
7. **Explainability**: Calculates SHAP summary plots.
8. **Registry**: Saves `.joblib` artifacts to `ml/models/` and updates `latest.json`.

## Scenario Testing

To test the model's performance on the 12 curated hackathon demo scenarios (which simulate real API payloads), run:

```bash
python ml/inference/scenario_tester.py
```

This will output the predicted risk score (0-100), risk level (Very Low to Critical), recommended action, and the top SHAP contributing features for each scenario.

## Retraining

To retrain the model with new data:
1. Replace or append to the CSV files in `datasets/synthetic/` and `datasets/reference/`.
2. Re-run `python ml/train.py`.
3. The registry automatically handles versioning using timestamped filenames (e.g., `LightGBM_20260702_143000_model.joblib`), ensuring you never overwrite past models. Downstream applications automatically pick up the new model via `latest.json`.
