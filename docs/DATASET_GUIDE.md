# NIRNAY: Synthetic Dataset Guide

This document explains the synthetic data architecture for the NIRNAY Agentic Financial Decision Intelligence project. This data powers the machine learning models, LangGraph agents, analytics dashboards, and frontend UI.

## Folder Structure Overview

```text
datasets/
├── synthetic/          # Core generated entities and transactions
├── processed/          # Aggregated analytics and ML feature matrices
├── reference/          # Reference tables (scam patterns, merchant rep)
├── demo/               # Self-contained scenario JSONs for the UI Demo Mode
└── raw/                # Reserved for any future external/real data imports
```

---

## 1. Core Entities (synthetic/)

### `customers.csv`
Represents the retail banking user base.
- **Fields:** `customer_id`, `full_name`, `gender`, `age`, `dob`, `occupation`, `employment_type`, `annual_income`, `monthly_income`, `city`, `state`, `country`, `pincode`, `customer_since`, `account_type`, `risk_profile`, `kyc_status`, `marital_status`, `education`, `preferred_language`, `preferred_transaction_time`, `credit_score`, `average_monthly_spending`, `average_transfer_amount`, `average_balance`, `registered_device_id`, `device_type`, `email`, `phone`
- **Usage:** Used by the UI for the user profile, by the Context Agent to understand the user's demographic baseline, and for ML feature scaling.
- **Methodology:** Generated with realistic demographic correlations (e.g., income correlates with occupation and age; credit score correlates with income).

### `accounts.csv`
Represents the bank accounts owned by customers.
- **Fields:** `account_id`, `customer_id`, `bank_name`, `branch`, `account_number`, `ifsc`, `account_type`, `current_balance`, `available_balance`, `account_status`, `opened_date`
- **Usage:** UI display, transaction routing, and balance validation.

### `recipients.csv`
Represents the people and businesses the customer transacts with.
- **Fields:** `recipient_id`, `customer_id`, `recipient_name`, `recipient_bank`, `recipient_account_number`, `recipient_ifsc`, `recipient_type`, `relationship`, `trusted_recipient`, `first_added`, `last_transaction_date`, `transaction_count`
- **Usage:** Used heavily in ML feature engineering (`is_trusted`, `new_recipient`) and by the Decision Intelligence Agent to evaluate counterparty risk.

### `merchants.csv`
Global directory of registered merchants.
- **Fields:** `merchant_id`, `merchant_name`, `merchant_category`, `merchant_city`, `merchant_state`, `merchant_country`, `trust_score`, `verified`, `registration_status`, `merchant_risk_level`, `reported_scam_count`
- **Usage:** Validating merchant transactions.

---

## 2. Transactions & Intelligence (synthetic/)

### `transactions.csv`
The core ledger of all financial movements.
- **Fields:** `transaction_id`, `customer_id`, `account_id`, `recipient_id`, `merchant_id`, `transaction_type`, `payment_channel`, `category`, `merchant_name`, `amount`, `currency`, `timestamp`, `day_of_week`, `hour`, `device_type`, `device_location`, `geo_latitude`, `geo_longitude`, `transaction_status`, `remarks`
- **Usage:** Drives the entire pipeline. Used by UI transaction history, analytics dashboards, and ML model inference.
- **Methodology:** 95% legitimate transactions based on income-proportional scaling and categorical distributions. 5% suspicious transactions with elevated amounts, unusual times, and scam-indicative remarks.

### `risk_events.csv`
Records of transactions flagged by the system as potentially risky.
- **Fields:** `risk_event_id`, `transaction_id`, `customer_id`, `risk_score`, `risk_level`, `risk_type`, `trigger_reason`, `ml_probability`, `explanation`, `confidence_score`, `agent_decision`, `customer_response`, `final_outcome`
- **Usage:** Powers the risk dashboard, triggers LangGraph agent interventions, and serves as the primary evaluation set for the decision engine.

### `conversations.csv`
Transcripts of AI agent conversations with customers regarding risky transactions.
- **Fields:** `conversation_id`, `customer_id`, `transaction_id`, `conversation_turn`, `speaker`, `message`, `intent`, `sentiment`, `agent_action`, `conversation_timestamp`
- **Usage:** Provides historical training data for the LangGraph Conversation Agent and UI transcripts for the Decision Timeline.

### `feedback.csv`
Customer feedback on the system's interventions.
- **Fields:** `feedback_id`, `customer_id`, `transaction_id`, `conversation_id`, `customer_action`, `verified`, `cancelled`, `continued`, `feedback_rating`, `feedback_comment`, `timestamp`
- **Usage:** Provides ground-truth labels (`fraud_confirmed`, `false_alarm`) for the ML feedback loop and retraining pipeline.

---

## 3. Analytics & ML (processed/ & reference/)

### `ml_features.csv` (processed/)
The engineered feature matrix ready for XGBoost training.
- **Fields:** 20+ engineered features including `amount_deviation`, `transaction_velocity`, `behavior_score`, `recipient_risk_score`, and the target `risk_label`.
- **Usage:** Direct input for Phase 2 (Machine Learning Pipeline).

### `behavior_profiles.csv` (processed/)
Aggregated behavioral baselines for each customer.
- **Fields:** `average_daily_transactions`, `favorite_categories`, `usual_location`, `monthly_spending_variance`, `night_transaction_ratio`, etc.
- **Usage:** Used by the Context Agent for real-time anomaly detection without needing to scan the full transaction history.

### `dashboard_metrics.csv` (processed/)
Daily aggregated metrics.
- **Fields:** `date`, `daily_transactions`, `high_risk_transactions`, `fraud_prevented`, `customer_trust_score`, etc.
- **Usage:** Powers the Admin / Behaviour Dashboard charts in the frontend.

### `scam_patterns.csv` (reference/)
A taxonomy of known financial fraud patterns.
- **Fields:** `pattern_id`, `pattern_name`, `category`, `description`, `behavior_signature`, `risk_level`, `recommended_action`, `expected_agent_response`
- **Usage:** Used by the Decision Intelligence Agent to match transaction signatures against known vectors (e.g., Investment Scams, Romance Scams, Deepfakes).

---

## 4. Demo Scenarios (demo/)
A collection of 12 self-contained JSON files (e.g., `investment_scam.json`, `deepfake_scam.json`).
- **Usage:** Injected directly into the Frontend during Hackathon presentations to guarantee a flawless, zero-latency demonstration of specific agentic capabilities without relying on live backend generation.
