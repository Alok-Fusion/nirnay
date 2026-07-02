import pytest
import pandas as pd
import numpy as np
from ml.feature_engineering.pipeline import FeatureEngineer
from ml.preprocessing.pipeline import Preprocessor

def get_dummy_data():
    return pd.DataFrame([{
        "transaction_id": "TXN123",
        "amount": 50000,
        "average_transaction": 5000,
        "current_balance": 100000,
        "timestamp": "2026-07-02T14:30:00",
        "trusted_recipient": True,
        "transaction_count": 10,
        "trust_score": 80,
        "reported_scam_count_rep": 0,
        "favorite_categories": "Transfer,Shopping",
        "category": "Transfer",
        "usual_location": "Mumbai",
        "city": "Mumbai",
        "usual_device": "Mobile",
        "device_type_x": "Mobile",
        "risk_profile": "Low",
        "digital_payment_ratio": 0.9,
        "transaction_type": "Debit",
        "payment_channel": "UPI",
        "risk_label": 0
    }])

def test_feature_engineering():
    df = get_dummy_data()
    fe = FeatureEngineer()
    
    df_out = fe.fit_transform(df)
    
    assert 'amount_deviation' in df_out.columns
    assert 'balance_ratio' in df_out.columns
    
    # Check derived logic
    assert df_out.iloc[0]['amount_deviation'] == 10.0
    assert df_out.iloc[0]['balance_ratio'] == 0.5
    assert df_out.iloc[0]['is_favorite_category'] == 1
    assert df_out.iloc[0]['location_deviation'] == 0
    assert df_out.iloc[0]['device_deviation'] == 0

def test_preprocessing():
    df = get_dummy_data()
    fe = FeatureEngineer()
    df_features = fe.fit_transform(df)
    
    preprocessor = Preprocessor()
    # Mock fit on single sample just for shape validation
    df_processed = preprocessor.fit_transform(df_features)
    
    assert isinstance(df_processed, pd.DataFrame)
    assert not df_processed.isnull().values.any()
