"""
Data Loader Module
Responsible for reading raw CSV datasets generated in Phase 1.
"""
import os
import pandas as pd

# Directory setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
SYNTHETIC_DIR = os.path.join(DATASETS_DIR, "synthetic")
PROCESSED_DIR = os.path.join(DATASETS_DIR, "processed")
REFERENCE_DIR = os.path.join(DATASETS_DIR, "reference")

class DataLoader:
    def __init__(self, data_dir=DATASETS_DIR):
        self.synthetic_dir = os.path.join(data_dir, "synthetic")
        self.processed_dir = os.path.join(data_dir, "processed")
        self.reference_dir = os.path.join(data_dir, "reference")
        
    def load_customers(self) -> pd.DataFrame:
        return pd.read_csv(os.path.join(self.synthetic_dir, "customers.csv"))
        
    def load_accounts(self) -> pd.DataFrame:
        return pd.read_csv(os.path.join(self.synthetic_dir, "accounts.csv"))
        
    def load_recipients(self) -> pd.DataFrame:
        return pd.read_csv(os.path.join(self.synthetic_dir, "recipients.csv"))
        
    def load_merchants(self) -> pd.DataFrame:
        return pd.read_csv(os.path.join(self.synthetic_dir, "merchants.csv"))
        
    def load_merchant_reputation(self) -> pd.DataFrame:
        return pd.read_csv(os.path.join(self.reference_dir, "merchant_reputation.csv"))
        
    def load_transactions(self) -> pd.DataFrame:
        return pd.read_csv(os.path.join(self.synthetic_dir, "transactions.csv"))
        
    def load_risk_events(self) -> pd.DataFrame:
        return pd.read_csv(os.path.join(self.synthetic_dir, "risk_events.csv"))
        
    def load_feedback(self) -> pd.DataFrame:
        return pd.read_csv(os.path.join(self.synthetic_dir, "feedback.csv"))
        
    def load_behavior_profiles(self) -> pd.DataFrame:
        return pd.read_csv(os.path.join(self.processed_dir, "behavior_profiles.csv"))
