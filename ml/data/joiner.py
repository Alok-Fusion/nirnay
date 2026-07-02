"""
Data Joiner Module
Responsible for merging datasets into a master training set and computing the target variable.
"""
import pandas as pd
from .loader import DataLoader

class DataJoiner:
    def __init__(self, loader: DataLoader = None):
        self.loader = loader or DataLoader()
        
    def create_master_dataset(self) -> pd.DataFrame:
        """
        Loads all required datasets, joins them on foreign keys, 
        and formulates the target variable (risk_label).
        """
        print("Loading datasets for join...")
        txn_df = self.loader.load_transactions()
        cust_df = self.loader.load_customers()
        acct_df = self.loader.load_accounts()
        recip_df = self.loader.load_recipients()
        merch_df = self.loader.load_merchants()
        merch_rep_df = self.loader.load_merchant_reputation()
        beh_df = self.loader.load_behavior_profiles()
        risk_df = self.loader.load_risk_events()
        feedback_df = self.loader.load_feedback()
        
        # 1. Start with transactions
        master = txn_df.copy()
        print(f"Base transactions: {master.shape[0]}")
        
        # 2. Join Customers
        master = master.merge(cust_df, on="customer_id", how="left")
        
        # 3. Join Accounts
        master = master.merge(acct_df, on=["account_id", "customer_id"], how="left")
        
        # 4. Join Recipients (Left join as some txns are to merchants)
        master = master.merge(recip_df, on=["recipient_id", "customer_id"], how="left")
        
        # 5. Join Merchants
        master = master.merge(merch_df, on="merchant_id", how="left")
        
        # 6. Join Merchant Reputation
        master = master.merge(merch_rep_df, on="merchant_id", how="left", suffixes=("", "_rep"))
        
        # 7. Join Behavior Profiles
        master = master.merge(beh_df, on="customer_id", how="left", suffixes=("", "_beh"))
        
        # 8. Create Target Variable (Risk Label)
        # We define unsafe (1) as transactions flagged High/Critical in risk_events
        # EXCEPT if feedback marked it as a false alarm (e.g., customer verified it's safe).
        # We will simplify by just taking High/Critical from risk_events as 1, others 0.
        
        risk_df['is_flagged'] = risk_df['risk_level'].isin(['High', 'Critical']).astype(int)
        
        # If feedback exists and says verified (safe), we can override.
        if not feedback_df.empty:
            override = feedback_df[['transaction_id', 'verified']].copy()
            risk_df = risk_df.merge(override, on="transaction_id", how="left")
            # If verified == True, it's safe (0)
            risk_df.loc[risk_df['verified'] == True, 'is_flagged'] = 0
            
        target_df = risk_df[['transaction_id', 'is_flagged']]
        
        # Merge target to master
        master = master.merge(target_df, on="transaction_id", how="left")
        
        # Fill NaN targets with 0 (safe)
        master['risk_label'] = master['is_flagged'].fillna(0).astype(int)
        master.drop(columns=['is_flagged'], inplace=True, errors='ignore')
        
        print(f"Master dataset created with shape: {master.shape}")
        return master
