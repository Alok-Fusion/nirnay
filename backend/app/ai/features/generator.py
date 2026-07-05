from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Dict, Any
from backend.app.models.transaction import Transaction
from backend.app.models.account import Account
from backend.app.models.recipient import Recipient
from backend.app.models.user import User
import math

class FeatureGenerator:
    """
    Generates ML features dynamically from the database using SQL aggregations.
    This guarantees that the ML Risk Engine always receives every required feature.
    """
    
    @staticmethod
    def generate(db: Session, user_id: int, account_id: int, recipient_id: int, current_amount: float) -> Dict[str, Any]:
        now = datetime.utcnow()
        
        # 1. Base Entity Fetches
        user = db.query(User).filter(User.id == user_id).first()
        account = db.query(Account).filter(Account.id == account_id).first()
        recipient = db.query(Recipient).filter(Recipient.id == recipient_id).first()
        
        from backend.app.models.behavior_profile import BehaviorProfile
        profile = db.query(BehaviorProfile).filter(BehaviorProfile.user_id == user_id).first()
        
        # Base fallback
        if not user or not account or not recipient:
            return FeatureGenerator._default_features()
            
        # 2. Temporal Aggregations
        thirty_days_ago = now - timedelta(days=30)
        seven_days_ago = now - timedelta(days=7)
        one_day_ago = now - timedelta(days=1)
        one_hour_ago = now - timedelta(hours=1)
        
        # All historical transactions for this account
        history_query = db.query(Transaction).filter(Transaction.account_id == account_id)
        
        from backend.app.models.transaction import TransactionState
        daily_spent_sum = db.query(func.sum(Transaction.amount)).filter(
            Transaction.account_id == account_id,
            Transaction.status == TransactionState.COMPLETED,
            Transaction.created_at >= one_day_ago
        ).scalar() or 0.0
        
        trust_level = profile.trust_level if profile else "NEW"
        limit_map = {
            "NEW": 1000.0,
            "LEARNING": 5000.0,
            "ESTABLISHED": 25000.0,
            "TRUSTED": 1000000.0
        }
        daily_limit = limit_map.get(trust_level, 1000.0)
        
        # Compute counts and averages via SQL
        # Fallback to 0 if None
        thirty_days_stats = db.query(
            func.count(Transaction.id),
            func.avg(Transaction.amount)
        ).filter(
            Transaction.account_id == account_id,
            Transaction.created_at >= thirty_days_ago
        ).first()
        
        tx_last_30_days = thirty_days_stats[0] or 0
        avg_tx_last_30_days = thirty_days_stats[1] or 0.0
        
        # Weekly
        tx_last_week = db.query(func.count(Transaction.id)).filter(
            Transaction.account_id == account_id, Transaction.created_at >= seven_days_ago
        ).scalar() or 0
        
        # Daily
        tx_last_day = db.query(func.count(Transaction.id)).filter(
            Transaction.account_id == account_id, Transaction.created_at >= one_day_ago
        ).scalar() or 0
        
        # Hourly
        tx_last_hour = db.query(func.count(Transaction.id)).filter(
            Transaction.account_id == account_id, Transaction.created_at >= one_hour_ago
        ).scalar() or 0
        
        # Last transaction time
        last_tx = db.query(Transaction).filter(Transaction.account_id == account_id).order_by(Transaction.created_at.desc()).first()
        time_since_last_tx_hours = (now - last_tx.created_at.replace(tzinfo=None)).total_seconds() / 3600.0 if last_tx else 24.0 * 30 # Default 30 days
        
        # Recipient specific stats
        recipient_tx_count = db.query(func.count(Transaction.id)).filter(
            Transaction.account_id == account_id, Transaction.recipient_id == recipient_id
        ).scalar() or 0
        
        # Derived values
        balance_before = account.balance
        balance_after = balance_before - current_amount
        remaining_balance_ratio = balance_after / (balance_before + 1.0) # avoid division by zero
        amount_ratio = current_amount / (avg_tx_last_30_days + 1.0)
        
        # Age
        account_age_days = (now - account.created_at.replace(tzinfo=None)).days if account.created_at else 100
        recipient_first_seen_days = (now - recipient.created_at.replace(tzinfo=None)).days if recipient.created_at else 0
        
        # Context flags
        hour_of_day = now.hour
        is_night = 1.0 if (hour_of_day < 6 or hour_of_day > 22) else 0.0
        is_weekend = 1.0 if now.weekday() >= 5 else 0.0
        
        # Compile all features
        features = {
            "daily_spent_sum": float(daily_spent_sum),
            "daily_limit": float(daily_limit),
            "limit_exceeded": 1.0 if (daily_spent_sum + current_amount) > daily_limit else 0.0,
            "average_transaction": float(profile.avg_transaction_amount) if profile else avg_tx_last_30_days,
            "average_daily_transaction": float(profile.average_daily_transactions) if profile else (avg_tx_last_30_days / 30.0 if tx_last_30_days > 0 else 0.0),
            "average_weekly_transaction": float(profile.avg_transaction_amount / 4.0) if profile else (avg_tx_last_30_days / 4.0 if tx_last_30_days > 0 else 0.0),
            "average_monthly_transaction": float(profile.avg_transaction_amount) if profile else avg_tx_last_30_days,
            "average_transaction_last_30_days": float(profile.avg_transaction_amount) if profile else avg_tx_last_30_days,
            "transaction_frequency": float(profile.transaction_count / 30.0) if profile else (tx_last_30_days / 30.0),
            "transactions_last_hour": tx_last_hour,
            "transactions_last_day": tx_last_day,
            "transactions_last_week": tx_last_week,
            "time_since_last_transaction": time_since_last_tx_hours,
            "recipient_transfer_count": recipient_tx_count,
            "recipient_first_seen_days": recipient_first_seen_days,
            "trusted_recipient": 1.0 if (recipient.is_trusted or (profile and recipient_id in (profile.trusted_recipients or []))) else 0.0,
            "recipient_risk": 0.0 if recipient.is_trusted else (1.0 if recipient_tx_count == 0 else 0.5),
            "account_age_days": float(account_age_days),
            "customer_age": 35.0, # Mock as user table doesn't have age
            "salary_band": 3.0,
            "occupation_score": 0.8,
            "balance_before": balance_before,
            "balance_after": balance_after,
            "remaining_balance_ratio": remaining_balance_ratio,
            "amount_ratio": current_amount / ((profile.avg_transaction_amount if profile and profile.avg_transaction_amount else avg_tx_last_30_days) + 1.0),
            "historical_risk": float(profile.historical_risk) if profile else 0.1,
            "behaviour_score": float((profile.trust_score or 50.0) / 100.0) if profile else 0.9,
            "device_score": 1.0,
            "location_score": 1.0,
            "velocity_score": min(tx_last_hour / 2.0, 1.0),
            "merchant_score": 1.0,
            "failed_login_attempts": 0.0,
            "night_transaction": is_night,
            "holiday_transaction": 0.0,
            "weekend_transaction": is_weekend
        }
        
        return features
        
    @staticmethod
    def _default_features() -> Dict[str, Any]:
        """Returns safe default zeroes for all required features if database lookups fail."""
        return {
            "average_transaction": 0.0, "average_daily_transaction": 0.0, "average_weekly_transaction": 0.0,
            "average_monthly_transaction": 0.0, "average_transaction_last_30_days": 0.0, "transaction_frequency": 0.0,
            "transactions_last_hour": 0.0, "transactions_last_day": 0.0, "transactions_last_week": 0.0,
            "time_since_last_transaction": 1000.0, "recipient_transfer_count": 0.0, "recipient_first_seen_days": 0.0,
            "trusted_recipient": 0.0, "recipient_risk": 1.0, "account_age_days": 0.0, "customer_age": 30.0,
            "salary_band": 2.0, "occupation_score": 0.5, "balance_before": 0.0, "balance_after": 0.0,
            "remaining_balance_ratio": 0.0, "amount_ratio": 1.0, "historical_risk": 0.5, "behaviour_score": 0.5,
            "device_score": 0.5, "location_score": 0.5, "velocity_score": 0.5, "merchant_score": 0.5,
            "failed_login_attempts": 0.0, "night_transaction": 0.0, "holiday_transaction": 0.0,
            "weekend_transaction": 0.0
        }
