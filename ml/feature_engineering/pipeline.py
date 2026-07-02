"""
Feature Engineering Pipeline
Generates all required ML features from the raw joined master dataset.
"""
import pandas as pd
import numpy as np

class FeatureEngineer:
    def __init__(self):
        pass
        
    def fit(self, X, y=None):
        return self
        
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies feature engineering to the master dataset.
        Returns a DataFrame ready for preprocessing.
        """
        print("Starting feature engineering...")
        X = df.copy()
        
        # ── 1. Amount & Spending Features ─────────────────────────────────────
        X['amount'] = pd.to_numeric(X['amount'], errors='coerce').fillna(0)
        X['average_transaction'] = pd.to_numeric(X['average_transaction'], errors='coerce').fillna(1)
        
        X['amount_deviation'] = X['amount'] / X['average_transaction'].replace(0, 1)
        
        X['current_balance'] = pd.to_numeric(X['current_balance'], errors='coerce').fillna(0)
        X['balance_ratio'] = X['amount'] / X['current_balance'].replace(0, 1)
        # Cap balance ratio
        X['balance_ratio'] = X['balance_ratio'].clip(upper=10)
        
        # ── 2. Time & Date Features ───────────────────────────────────────────
        X['timestamp'] = pd.to_datetime(X['timestamp'], errors='coerce')
        X['hour_of_day'] = X['timestamp'].dt.hour.fillna(0)
        X['day_of_week'] = X['timestamp'].dt.dayofweek.fillna(0)
        X['day_of_month'] = X['timestamp'].dt.day.fillna(1)
        
        X['is_weekend'] = X['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
        X['is_night_transaction'] = X['hour_of_day'].apply(lambda x: 1 if (x < 6 or x > 22) else 0)
        X['salary_week'] = X['day_of_month'].apply(lambda x: 1 if (x <= 7 or x >= 28) else 0)
        
        # ── 3. Recipient & Merchant Trust Features ────────────────────────────
        X['is_trusted_recipient'] = X['trusted_recipient'].fillna(False).astype(int)
        X['recipient_familiarity'] = pd.to_numeric(X['transaction_count'], errors='coerce').fillna(0)
        
        X['merchant_trust_score'] = pd.to_numeric(X['trust_score'], errors='coerce').fillna(50)
        X['merchant_scam_reports'] = pd.to_numeric(X['reported_scam_count_rep'], errors='coerce').fillna(0)
        
        # ── 4. Behavior Deviation Features ────────────────────────────────────
        # Favorite categories match
        X['favorite_categories'] = X['favorite_categories'].fillna("")
        X['category'] = X['category'].fillna("Unknown")
        X['is_favorite_category'] = X.apply(lambda row: 1 if row['category'] in str(row['favorite_categories']) else 0, axis=1)
        
        X['usual_location'] = X['usual_location'].fillna("Unknown")
        X['city'] = X['city'].fillna("Unknown")
        X['location_deviation'] = (X['city'] != X['usual_location']).astype(int)
        
        X['usual_device'] = X['usual_device'].fillna("Unknown")
        X['device_type'] = X['device_type_x'].fillna("Unknown") if 'device_type_x' in X.columns else X['device_type'].fillna("Unknown")
        X['device_deviation'] = (X['device_type'] != X['usual_device']).astype(int)
        
        # ── 5. Derived Risk Scores (Simulated based on profile) ───────────────
        risk_map = {'Low': 1, 'Medium': 2, 'High': 3}
        X['customer_risk_profile_score'] = X['risk_profile'].map(risk_map).fillna(2)
        
        X['digital_payment_ratio'] = pd.to_numeric(X['digital_payment_ratio'], errors='coerce').fillna(0.5)
        
        # Feature list explicitly requested
        cols_to_keep = [
            'transaction_id', 'amount', 'amount_deviation', 'balance_ratio', 
            'hour_of_day', 'day_of_week', 'is_weekend', 'is_night_transaction', 'salary_week',
            'is_trusted_recipient', 'recipient_familiarity', 
            'merchant_trust_score', 'merchant_scam_reports',
            'is_favorite_category', 'location_deviation', 'device_deviation',
            'customer_risk_profile_score', 'digital_payment_ratio',
            'transaction_type', 'payment_channel', 'category', 'risk_label'
        ]
        
        # Drop columns not in the list (but keep risk_label and transaction_id)
        # Ensure they exist
        existing_cols = [c for c in cols_to_keep if c in X.columns]
        
        print(f"Feature engineering complete. {len(existing_cols)} features generated.")
        return X[existing_cols]

    def fit_transform(self, X, y=None):
        return self.fit(X).transform(X)
