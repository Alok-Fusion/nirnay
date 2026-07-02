"""
NIRNAY — Master Data Generation Pipeline
==========================================
Executes the entire synthetic data engineering pipeline for the NIRNAY project.
Generates all datasets, demo scenarios, and statistical summaries.

Usage:
    python generate_data.py
"""

import os
import sys
import time
import json
import numpy as np
import pandas as pd
from datetime import datetime

# Import configuration and generators
from scripts.config import SEED
from scripts.generators.entities import (
    generate_customers,
    generate_accounts,
    generate_recipients,
    generate_merchants,
    generate_merchant_reputation
)
from scripts.generators.transactions import generate_transactions
from scripts.generators.intelligence import (
    generate_scam_patterns,
    generate_risk_events,
    generate_conversations,
    generate_feedback
)
from scripts.generators.analytics import (
    generate_behavior_profiles,
    generate_dashboard_metrics,
    generate_ml_features
)
from scripts.generators.demo import generate_demo_scenarios

# Directory setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
SYNTHETIC_DIR = os.path.join(DATASETS_DIR, "synthetic")
REFERENCE_DIR = os.path.join(DATASETS_DIR, "reference")
PROCESSED_DIR = os.path.join(DATASETS_DIR, "processed")
DEMO_DIR = os.path.join(DATASETS_DIR, "demo")

def setup_directories():
    """Ensure all target directories exist."""
    print(f"Setting up directories in {DATASETS_DIR}...")
    os.makedirs(SYNTHETIC_DIR, exist_ok=True)
    os.makedirs(REFERENCE_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(DEMO_DIR, exist_ok=True)
    
def generate_all_data():
    """Execute the full data generation pipeline."""
    print("=" * 60)
    print("NIRNAY — Agentic Financial Decision Intelligence")
    print("Phase 1: Synthetic Data Generation Pipeline")
    print("=" * 60)
    
    start_time = time.time()
    rng = np.random.default_rng(SEED)
    
    # ── 1. Reference Data ──────────────────────────────────────────
    print("\n[1/4] Generating Reference Data...")
    scam_patterns_df = generate_scam_patterns(rng)
    scam_patterns_df.to_csv(os.path.join(REFERENCE_DIR, "scam_patterns.csv"), index=False)
    print(f"  [OK] scam_patterns.csv      ({len(scam_patterns_df)} records)")
    
    # ── 2. Core Entities ───────────────────────────────────────────
    print("\n[2/4] Generating Core Entities...")
    
    customers_df = generate_customers(rng)
    customers_df.to_csv(os.path.join(SYNTHETIC_DIR, "customers.csv"), index=False)
    print(f"  [OK] customers.csv          ({len(customers_df)} records)")
    
    accounts_df = generate_accounts(rng, customers_df)
    accounts_df.to_csv(os.path.join(SYNTHETIC_DIR, "accounts.csv"), index=False)
    print(f"  [OK] accounts.csv           ({len(accounts_df)} records)")
    
    recipients_df = generate_recipients(rng, customers_df)
    recipients_df.to_csv(os.path.join(SYNTHETIC_DIR, "recipients.csv"), index=False)
    print(f"  [OK] recipients.csv         ({len(recipients_df)} records)")
    
    merchants_df = generate_merchants(rng)
    merchants_df.to_csv(os.path.join(SYNTHETIC_DIR, "merchants.csv"), index=False)
    print(f"  [OK] merchants.csv          ({len(merchants_df)} records)")
    
    merchant_rep_df = generate_merchant_reputation(rng, merchants_df)
    merchant_rep_df.to_csv(os.path.join(REFERENCE_DIR, "merchant_reputation.csv"), index=False)
    print(f"  [OK] merchant_rep.csv       ({len(merchant_rep_df)} records)")
    
    # ── 3. Transactions & Risk Intelligence ────────────────────────
    print("\n[3/4] Generating Transactions & Intelligence...")
    
    transactions_df = generate_transactions(rng, customers_df, accounts_df, recipients_df, merchants_df)
    transactions_df.to_csv(os.path.join(SYNTHETIC_DIR, "transactions.csv"), index=False)
    print(f"  [OK] transactions.csv       ({len(transactions_df)} records)")
    
    risk_events_df = generate_risk_events(rng, transactions_df, customers_df, recipients_df, scam_patterns_df)
    risk_events_df.to_csv(os.path.join(SYNTHETIC_DIR, "risk_events.csv"), index=False)
    print(f"  [OK] risk_events.csv        ({len(risk_events_df)} records)")
    
    conversations_df = generate_conversations(rng, risk_events_df, transactions_df)
    conversations_df.to_csv(os.path.join(SYNTHETIC_DIR, "conversations.csv"), index=False)
    print(f"  [OK] conversations.csv      ({len(conversations_df)} records)")
    
    feedback_df = generate_feedback(rng, risk_events_df, conversations_df)
    feedback_df.to_csv(os.path.join(SYNTHETIC_DIR, "feedback.csv"), index=False)
    print(f"  [OK] feedback.csv           ({len(feedback_df)} records)")
    
    # ── 4. Analytics, Features & Demo ──────────────────────────────
    print("\n[4/4] Generating Analytics, ML Features & Demos...")
    
    behavior_df = generate_behavior_profiles(rng, customers_df, transactions_df)
    behavior_df.to_csv(os.path.join(PROCESSED_DIR, "behavior_profiles.csv"), index=False)
    print(f"  [OK] behavior_profiles.csv  ({len(behavior_df)} records)")
    
    dashboard_df = generate_dashboard_metrics(rng, transactions_df, risk_events_df)
    dashboard_df.to_csv(os.path.join(PROCESSED_DIR, "dashboard_metrics.csv"), index=False)
    print(f"  [OK] dashboard_metrics.csv  ({len(dashboard_df)} records)")
    
    ml_features_df = generate_ml_features(rng, transactions_df, customers_df, recipients_df, behavior_df, merchants_df, risk_events_df)
    ml_features_df.to_csv(os.path.join(PROCESSED_DIR, "ml_features.csv"), index=False)
    print(f"  [OK] ml_features.csv        ({len(ml_features_df)} records)")
    
    demo_scenarios = generate_demo_scenarios(DEMO_DIR)
    print(f"  [OK] demo scenarios         ({len(demo_scenarios)} JSON files)")
    
    # ── Generate Dataset Statistics ────────────────────────────────
    print("\nGenerating Dataset Statistics...")
    stats = {
        "generation_timestamp": datetime.now().isoformat(),
        "random_seed": SEED,
        "record_counts": {
            "customers": len(customers_df),
            "accounts": len(accounts_df),
            "recipients": len(recipients_df),
            "merchants": len(merchants_df),
            "transactions": len(transactions_df),
            "risk_events": len(risk_events_df),
            "scam_patterns": len(scam_patterns_df),
            "conversations": len(conversations_df),
            "feedback": len(feedback_df),
            "ml_features": len(ml_features_df),
            "demo_scenarios": len(demo_scenarios)
        },
        "risk_distribution": risk_events_df['risk_level'].value_counts().to_dict() if not risk_events_df.empty else {},
        "transaction_distribution": transactions_df['category'].value_counts().to_dict()
    }
    
    with open(os.path.join(DATASETS_DIR, "dataset_statistics.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print("  [OK] dataset_statistics.json created")
    
    # ── Generate ER Diagram Overview (Markdown) ────────────────────
    er_overview = """# NIRNAY - Entity Relationship Overview

## Core Entities
- **Customers** (1) --- (1..N) **Accounts**
- **Customers** (1) --- (1..N) **Recipients**
- **Customers** (1) --- (1) **Behavior Profiles**

## Transactions & Intelligence
- **Transactions** (N) --- (1) **Customers**
- **Transactions** (N) --- (1) **Accounts**
- **Transactions** (N) --- (0..1) **Recipients**
- **Transactions** (N) --- (0..1) **Merchants**
- **Risk Events** (1) --- (1) **Transactions**
- **Conversations** (N) --- (1) **Transactions**
- **Feedback** (1) --- (1) **Transactions**

## Reference
- **Merchants** (1) --- (1) **Merchant Reputation**
- **Risk Events** (N) --- (1) **Scam Patterns**
"""
    with open(os.path.join(DATASETS_DIR, "ER_OVERVIEW.md"), "w", encoding="utf-8") as f:
        f.write(er_overview)
    print("  [OK] ER_OVERVIEW.md created")

    elapsed_time = time.time() - start_time
    print(f"\n============================================================")
    print(f"Data Generation Complete! [OK]")
    print(f"Total Execution Time: {elapsed_time:.2f} seconds")
    print(f"All datasets saved to: {DATASETS_DIR}")
    print(f"============================================================")

if __name__ == "__main__":
    setup_directories()
    generate_all_data()
