# Model Card: NIRNAY Decision Intelligence Engine

## Model Details
- **Architecture**: Ensembles of trees (LightGBM/XGBoost) optimized via RandomizedSearchCV.
- **Task**: Binary Classification.
- **Target**: Probability that a transaction represents an unsafe financial decision (1) vs a normal transaction (0).
- **Features**: 39 engineered features derived from customer behavior, recipient familiarity, temporal patterns, and transaction amounts.

## Intended Use
- **Primary Use Case**: To intercept potentially unsafe financial transactions (e.g., scams, coercion) in real-time before completion, generating a risk score that triggers Agentic AI interventions.
- **Out of Scope**: This model is NOT intended to replace traditional card-not-present fraud detection or anti-money laundering (AML) checks.

## Metrics
The model is evaluated using the following metrics on a 20% holdout test set:
- **ROC-AUC**: Primary metric for optimization, threshold-independent performance.
- **Precision**: High precision is required to minimize false positive interventions (which degrade user experience).
- **Recall**: High recall ensures we catch sophisticated scams.
- **F1-Score**: Harmonic mean of Precision and Recall.

*Detailed metrics and plots (ROC, PR, Confusion Matrix, Calibration) are generated automatically and saved to `ml/evaluation/plots/` during the training pipeline.*

## Data
- **Training Data**: 50,000 synthetic transactions spanning 1,000 customers.
- **Class Imbalance**: Highly imbalanced (approx. 95% Safe / 5% Unsafe). Addressed using `class_weight='balanced'` and scale_pos_weight.

## Explainability
- Local explanations are provided via SHAP (SHapley Additive exPlanations) TreeExplainer.
- For every inference call, the model outputs the top contributing factors that increased or decreased the risk, enabling the LangGraph Conversation Agent to provide transparent, human-readable justifications to the user.

## Limitations & Future Improvements
- **Limitation**: The model currently relies on synthetic behaviors. In a real-world scenario, continuous retraining pipelines are essential.
- **Future**: Incorporating real-time NLP embeddings from customer chat logs directly into the model to capture social engineering intent before the transaction is even initiated.
