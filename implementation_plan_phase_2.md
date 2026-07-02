# Phase 2: Machine Learning & Decision Intelligence Pipeline

This document outlines the architecture and execution plan for Phase 2: Machine Learning for the NIRNAY project. The objective is to build a production-quality, reproducible ML pipeline that predicts the probability of an unsafe financial decision, generating features from the raw datasets, training multiple models, selecting the best one, and generating SHAP explainability insights.

## User Review Required

> [!IMPORTANT]
> The target variable definition is critical. We will use `risk_events.csv` and `feedback.csv` to construct our ground truth labels. Specifically, we will treat high/critical risk events that were NOT false alarms as positive cases (1), and safe transactions / false alarms as negative cases (0). Please confirm if this target formulation aligns with the "unsafe financial decision" objective.

> [!WARNING]
> Training advanced tree models (XGBoost, LightGBM, Random Forest) with cross-validation and hyperparameter tuning on 50,000 records will take several minutes during execution.

## Proposed Architecture

We will implement a modular Python package structure in the `/ml` directory:

```text
ml/
├── data/                  # Data loading and joining logic
├── preprocessing/         # Imputation, scaling, encoding pipelines
├── feature_engineering/   # Feature derivation (velocity, ratios, deviations)
├── training/              # Model training, hyperparameter tuning, selection
├── evaluation/            # Metrics calculation, plot generation
├── explainability/        # SHAP integration (Global/Local explanations)
├── inference/             # Production inference wrapper
├── registry/              # Model saving, versioning, metadata tracking
├── utils/                 # Logging, config parsing, helpers
├── tests/                 # Unit testing
├── models/                # Saved model artifacts (.pkl, .joblib)
├── configs/               # ML configuration YAMLs
└── notebooks/             # Reserved for EDA / scratchpads
```

## Implementation Phases

### 1. Data Engineering & Feature Generation
- **Data Loading:** Join `transactions.csv`, `customers.csv`, `accounts.csv`, `recipients.csv`, `behavior_profiles.csv`, `merchants.csv`, `merchant_reputation.csv`, and `risk_events.csv`.
- **Feature Engineering:** Programmatically derive features requested (amount deviation, average spending ratio, transfer ratio, recipient familiarity/trust, transaction velocity, time-based features, behavior deviation score, digital payment ratio).
- **Target Variable:** Binary classification label (0 = Safe, 1 = Unsafe/Scam).

### 2. Preprocessing Pipeline
- **Scikit-Learn Pipelines:** Build modular `ColumnTransformer` pipelines.
- **Categorical:** One-Hot Encoding for low cardinality, Target Encoding / Ordinal for high cardinality.
- **Numerical:** RobustScaler (handles outliers) / StandardScaler.
- **Missing Values:** SimpleImputer (median for numeric, constant/mode for categorical).
- **Splitting:** Time-based or stratified 80/10/10 (Train/Validation/Test) split.

### 3. Model Training & Selection
- Implement unified model wrappers for:
  - Logistic Regression (Baseline)
  - Random Forest
  - XGBoost (Primary Focus)
  - LightGBM (if available via pip)
- Implement Automated Model Selection based on Validation ROC AUC or F1-Score.
- Perform Hyperparameter Optimization (RandomizedSearchCV) for the top model.

### 4. Evaluation & Explainability
- **Metrics:** Accuracy, Precision, Recall, F1 Score, ROC AUC.
- **Artifacts Generated:** Confusion Matrix, ROC Curve, Precision-Recall Curve, Feature Importance plots.
- **Explainable AI (SHAP):** Integrate `shap` library to generate:
  - Global Feature Importance summary plots.
  - Local Decision Waterfalls / Force plots for individual transaction inference.

### 5. Registry & Inference Engine
- **Model Registry:** Save trained models, preprocessing pipelines, and metadata (metrics, training time, version) into `ml/models/`.
- **Inference Wrapper (`predict.py` / `risk_model.py`):** An API-agnostic inference engine that takes raw dictionaries, applies preprocessing and feature engineering, predicts probability, assigns Risk Levels (0-100 mapped to Very Low - Critical), and outputs SHAP explanations and recommended actions.

### 6. Scenario Testing
- Feed the 12 generated JSON scenarios from `datasets/demo/` through the `InferenceEngine` to generate prediction reports and validate pipeline robustness.

### 7. Documentation & Testing
- Generate `ML_ARCHITECTURE.md`, `MODEL_CARD.md`, `FEATURE_GUIDE.md`, and `TRAINING_GUIDE.md` in `ml/docs/`.
- Implement `pytest` unit tests for feature engineering, preprocessing, and inference.

## Open Questions

- We will generate feature plots and evaluation curves as `.png` files in the `ml/evaluation/` directory. Should they also be rendered as markdown artifacts?
- I will install `xgboost`, `lightgbm`, `scikit-learn`, `shap`, `matplotlib`, `seaborn` in the existing `venv`. Is that acceptable?

## Verification Plan

### Automated Tests
- Run `pytest ml/tests/` to verify pipeline integrity, feature shapes, and inference contracts.

### Manual Verification
- Run the scenario tester (`python -m ml.inference.scenario_tester`) to print predictions for the 12 hackathon scenarios.
- Inspect the generated plots and `MODEL_CARD.md` to ensure realistic performance metrics (targeting AUC > 0.85 but not 1.0 to avoid overfitting).
