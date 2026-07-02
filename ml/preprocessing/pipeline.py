"""
Preprocessing Pipeline
Handles missing values, scaling numerical features, and encoding categorical features.
"""
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

class Preprocessor:
    def __init__(self):
        self.numerical_cols = [
            'amount', 'amount_deviation', 'balance_ratio', 
            'hour_of_day', 'day_of_week', 'is_weekend', 'is_night_transaction', 'salary_week',
            'is_trusted_recipient', 'recipient_familiarity', 
            'merchant_trust_score', 'merchant_scam_reports',
            'is_favorite_category', 'location_deviation', 'device_deviation',
            'customer_risk_profile_score', 'digital_payment_ratio'
        ]
        self.categorical_cols = [
            'transaction_type', 'payment_channel', 'category'
        ]
        
        # Build scikit-learn pipeline
        self.numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        self.categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', self.numeric_transformer, self.numerical_cols),
                ('cat', self.categorical_transformer, self.categorical_cols)
            ]
        )
        
    def fit(self, X: pd.DataFrame, y=None):
        # Ensure only the columns we need are passed to the preprocessor
        X_sub = X[self.numerical_cols + self.categorical_cols]
        self.preprocessor.fit(X_sub, y)
        return self
        
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_sub = X[self.numerical_cols + self.categorical_cols]
        transformed_array = self.preprocessor.transform(X_sub)
        
        # Reconstruct DataFrame with column names for SHAP explainability
        # Get feature names from OneHotEncoder
        cat_features = self.preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(self.categorical_cols)
        all_features = self.numerical_cols + list(cat_features)
        
        return pd.DataFrame(transformed_array, columns=all_features, index=X.index)

    def fit_transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        return self.fit(X, y).transform(X)
