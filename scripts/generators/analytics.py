"""
NIRNAY — Analytics & Feature Generators
========================================
Generates: behavior_profiles.csv, dashboard_metrics.csv,
           ml_features.csv (ML-ready engineered features)
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


# ──────────────────────────────────────────────────────────────────────
# BEHAVIOR PROFILES
# ──────────────────────────────────────────────────────────────────────
def generate_behavior_profiles(rng, customers_df, transactions_df):
    """
    Generate one behavior profile per customer derived from their
    transaction history. These profiles are used by the Context Agent
    and ML feature engineering.
    """
    records = []
    txn_df = transactions_df.copy()
    txn_df["amount"] = pd.to_numeric(txn_df["amount"], errors="coerce")
    txn_df["hour"] = pd.to_numeric(txn_df["hour"], errors="coerce")
    txn_df["timestamp"] = pd.to_datetime(txn_df["timestamp"])

    for _, cust in customers_df.iterrows():
        cust_id = cust["customer_id"]
        cust_txns = txn_df[txn_df["customer_id"] == cust_id]

        if len(cust_txns) == 0:
            # Generate synthetic profile from customer attributes
            avg_txn = cust["average_transfer_amount"]
            records.append({
                "customer_id": cust_id,
                "average_transaction": avg_txn,
                "maximum_transaction": int(avg_txn * 5),
                "minimum_transaction": max(int(avg_txn * 0.1), 50),
                "average_daily_transactions": round(rng.uniform(0.5, 3.0), 1),
                "favorite_categories": "Transfer,Utilities,Food & Dining",
                "favorite_transaction_hour": int(cust["preferred_transaction_time"].split(":")[0]),
                "usual_location": cust["city"],
                "usual_device": cust["device_type"],
                "average_balance": cust["average_balance"],
                "recipient_diversity": rng.integers(3, 10),
                "salary_day": rng.integers(1, 6),
                "monthly_spending_variance": round(rng.uniform(0.05, 0.30), 3),
                "weekend_spending_ratio": round(rng.uniform(0.15, 0.40), 3),
                "night_transaction_ratio": round(rng.uniform(0.01, 0.10), 3),
                "investment_frequency": round(rng.uniform(0, 5), 1),
                "cash_withdrawal_frequency": round(rng.uniform(0, 8), 1),
                "digital_payment_ratio": round(rng.uniform(0.60, 0.98), 3),
            })
            continue

        amounts = cust_txns["amount"].values
        hours = cust_txns["hour"].values

        # Favorite categories (top 3)
        cat_counts = cust_txns["category"].value_counts()
        fav_cats = ",".join(cat_counts.head(3).index.tolist())

        # Most common hour
        fav_hour = int(pd.Series(hours).mode().iloc[0]) if len(hours) > 0 else 14

        # Most common location
        loc_counts = cust_txns["device_location"].value_counts()
        usual_loc = loc_counts.index[0] if len(loc_counts) > 0 else cust["city"]

        # Most common device
        dev_counts = cust_txns["device_type"].value_counts()
        usual_dev = dev_counts.index[0] if len(dev_counts) > 0 else cust["device_type"]

        # Unique recipients
        recipient_div = cust_txns["recipient_id"].nunique()

        # Salary day detection (look for largest credit in a month)
        credits = cust_txns[cust_txns["transaction_type"] == "Credit"]
        if len(credits) > 0:
            salary_day = int(credits.loc[credits["amount"].idxmax(), "timestamp"].day)
            salary_day = min(salary_day, 28)
        else:
            salary_day = rng.integers(1, 6)

        # Weekend ratio
        weekend_txns = cust_txns[cust_txns["day_of_week"].isin(["Saturday", "Sunday"])]
        weekend_ratio = round(len(weekend_txns) / max(len(cust_txns), 1), 3)

        # Night ratio (23:00 - 05:00)
        night_txns = cust_txns[(cust_txns["hour"] >= 23) | (cust_txns["hour"] <= 4)]
        night_ratio = round(len(night_txns) / max(len(cust_txns), 1), 3)

        # Investment frequency (per month)
        inv_txns = cust_txns[cust_txns["category"] == "Investment"]
        months_span = max((cust_txns["timestamp"].max() - cust_txns["timestamp"].min()).days / 30, 1)
        inv_freq = round(len(inv_txns) / months_span, 1)

        # Monthly spending variance
        cust_txns_monthly = cust_txns.set_index("timestamp").resample("ME")["amount"].sum()
        if len(cust_txns_monthly) > 1:
            spending_var = round(cust_txns_monthly.std() / max(cust_txns_monthly.mean(), 1), 3)
        else:
            spending_var = round(rng.uniform(0.05, 0.25), 3)

        # Digital payment ratio
        digital_channels = ["UPI", "NEFT", "IMPS", "RTGS", "Net Banking", "Auto Debit"]
        digital_txns = cust_txns[cust_txns["payment_channel"].isin(digital_channels)]
        digital_ratio = round(len(digital_txns) / max(len(cust_txns), 1), 3)

        # Daily average
        days_span = max((cust_txns["timestamp"].max() - cust_txns["timestamp"].min()).days, 1)
        avg_daily = round(len(cust_txns) / days_span, 1)

        records.append({
            "customer_id": cust_id,
            "average_transaction": round(float(amounts.mean()), 2),
            "maximum_transaction": round(float(amounts.max()), 2),
            "minimum_transaction": round(float(amounts.min()), 2),
            "average_daily_transactions": avg_daily,
            "favorite_categories": fav_cats,
            "favorite_transaction_hour": fav_hour,
            "usual_location": usual_loc,
            "usual_device": usual_dev,
            "average_balance": cust["average_balance"],
            "recipient_diversity": int(recipient_div),
            "salary_day": salary_day,
            "monthly_spending_variance": float(spending_var),
            "weekend_spending_ratio": float(weekend_ratio),
            "night_transaction_ratio": float(night_ratio),
            "investment_frequency": float(inv_freq),
            "cash_withdrawal_frequency": round(rng.uniform(0, 8), 1),
            "digital_payment_ratio": float(digital_ratio),
        })

    return pd.DataFrame(records)


# ──────────────────────────────────────────────────────────────────────
# DASHBOARD METRICS
# ──────────────────────────────────────────────────────────────────────
def generate_dashboard_metrics(rng, transactions_df, risk_events_df):
    """
    Generate daily aggregate metrics for the analytics dashboard.
    """
    records = []
    txn_df = transactions_df.copy()
    txn_df["timestamp"] = pd.to_datetime(txn_df["timestamp"])
    txn_df["date"] = txn_df["timestamp"].dt.date
    txn_df["amount"] = pd.to_numeric(txn_df["amount"], errors="coerce")

    risk_df = risk_events_df.copy()
    risk_txn_ids = set(risk_df["transaction_id"].values)

    # Group transactions by date
    daily_groups = txn_df.groupby("date")

    for date, group in daily_groups:
        n_txns = len(group)
        volume = group["amount"].sum()
        avg_amount = group["amount"].mean()

        # Count risk events for this day's transactions
        day_txn_ids = set(group["transaction_id"].values)
        day_risk = risk_df[risk_df["transaction_id"].isin(day_txn_ids)]

        high_risk = len(day_risk[day_risk["risk_level"].isin(["High", "Critical"])])
        medium_risk = len(day_risk[day_risk["risk_level"] == "Medium"])

        cancelled = len(group[group["transaction_status"] == "Cancelled"])
        verified = len(day_risk[day_risk["customer_response"].isin(
            ["Verified and Proceeded", "Proceeded"]
        )]) if len(day_risk) > 0 else 0

        prevented = len(day_risk[day_risk["final_outcome"] == "Prevented"]) if len(day_risk) > 0 else 0

        # Customer trust score: inverse of risk ratio
        risk_ratio = (high_risk + medium_risk) / max(n_txns, 1)
        trust_score = round(np.clip(1.0 - risk_ratio * 5, 0.5, 1.0), 3)

        records.append({
            "date": str(date),
            "daily_transactions": n_txns,
            "daily_transaction_volume": round(volume, 2),
            "average_transaction_amount": round(avg_amount, 2),
            "high_risk_transactions": high_risk,
            "medium_risk_transactions": medium_risk,
            "cancelled_transactions": cancelled,
            "verified_transactions": verified,
            "fraud_prevented": prevented,
            "customer_trust_score": trust_score,
        })

    return pd.DataFrame(records)


# ──────────────────────────────────────────────────────────────────────
# ML FEATURE ENGINEERING
# ──────────────────────────────────────────────────────────────────────
def generate_ml_features(rng, transactions_df, customers_df, recipients_df,
                         behavior_df, merchants_df, risk_events_df):
    """
    Generate an ML-ready feature matrix for every transaction.
    Each row = one transaction with engineered features + binary label.
    """
    txn_df = transactions_df.copy()
    txn_df["amount"] = pd.to_numeric(txn_df["amount"], errors="coerce")
    txn_df["hour"] = pd.to_numeric(txn_df["hour"], errors="coerce")
    txn_df["timestamp"] = pd.to_datetime(txn_df["timestamp"])

    # Lookup maps
    cust_income = dict(zip(customers_df["customer_id"], customers_df["monthly_income"]))
    cust_avg_spend = dict(zip(customers_df["customer_id"], customers_df["average_monthly_spending"]))
    cust_avg_txn = dict(zip(customers_df["customer_id"], customers_df["average_transfer_amount"]))
    cust_credit = dict(zip(customers_df["customer_id"], customers_df["credit_score"]))
    cust_risk_prof = dict(zip(customers_df["customer_id"], customers_df["risk_profile"]))
    cust_device = dict(zip(customers_df["customer_id"], customers_df["device_type"]))
    cust_city = dict(zip(customers_df["customer_id"], customers_df["city"]))

    rec_trusted = dict(zip(recipients_df["recipient_id"], recipients_df["trusted_recipient"]))
    rec_rel = dict(zip(recipients_df["recipient_id"], recipients_df["relationship"]))
    rec_txn_count = dict(zip(recipients_df["recipient_id"], recipients_df["transaction_count"]))
    rec_first_added = dict(zip(recipients_df["recipient_id"], recipients_df["first_added"]))

    beh_avg_txn = dict(zip(behavior_df["customer_id"], behavior_df["average_transaction"]))
    beh_max_txn = dict(zip(behavior_df["customer_id"], behavior_df["maximum_transaction"]))
    beh_weekend = dict(zip(behavior_df["customer_id"], behavior_df["weekend_spending_ratio"]))
    beh_night = dict(zip(behavior_df["customer_id"], behavior_df["night_transaction_ratio"]))
    beh_digital = dict(zip(behavior_df["customer_id"], behavior_df["digital_payment_ratio"]))

    mer_trust = dict(zip(merchants_df["merchant_id"], merchants_df["trust_score"]))
    mer_risk = dict(zip(merchants_df["merchant_id"], merchants_df["merchant_risk_level"]))

    # Risk event transactions (labels)
    risk_txn_set = set(risk_events_df["transaction_id"].values)
    risk_levels = dict(zip(risk_events_df["transaction_id"], risk_events_df["risk_level"]))
    risk_outcomes = dict(zip(risk_events_df["transaction_id"], risk_events_df["final_outcome"]))

    # Indian holidays (approximate)
    holidays = {
        datetime(2025, 1, 26), datetime(2025, 3, 14), datetime(2025, 8, 15),
        datetime(2025, 10, 2), datetime(2025, 10, 20), datetime(2025, 10, 23),
        datetime(2025, 11, 1), datetime(2025, 11, 12), datetime(2025, 12, 25),
        datetime(2026, 1, 26), datetime(2026, 3, 14), datetime(2026, 3, 30),
        datetime(2026, 4, 14), datetime(2026, 5, 1), datetime(2026, 6, 17),
    }

    # Sort by customer + timestamp for velocity calculation
    txn_df = txn_df.sort_values(["customer_id", "timestamp"]).reset_index(drop=True)

    features = []
    prev_cust = None
    prev_time = None

    for idx, txn in txn_df.iterrows():
        cust_id = txn["customer_id"]
        amount = txn["amount"]
        hour = txn["hour"]
        rec_id = txn.get("recipient_id")
        mer_id = txn.get("merchant_id")
        txn_time = txn["timestamp"]

        # Amount deviation from customer average
        avg_amt = beh_avg_txn.get(cust_id, cust_avg_txn.get(cust_id, 5000))
        max_amt = beh_max_txn.get(cust_id, avg_amt * 5)
        amount_deviation = round((amount - avg_amt) / max(avg_amt, 1), 4)

        # Recipient features
        is_trusted = bool(rec_trusted.get(rec_id, False)) if pd.notna(rec_id) else False
        relationship = rec_rel.get(rec_id, "Unknown") if pd.notna(rec_id) else "Unknown"
        rec_freq = rec_txn_count.get(rec_id, 0) if pd.notna(rec_id) else 0
        new_recipient = 1 if rec_freq <= 1 and relationship == "Unknown" else 0

        # Time features
        night_txn = 1 if (hour >= 23 or hour <= 4) else 0
        weekend_txn = 1 if txn["day_of_week"] in ("Saturday", "Sunday") else 0
        holiday_txn = 1 if txn_time.date() in {h.date() for h in holidays} else 0

        # Salary week (within 5 days of 1st of month)
        salary_week = 1 if txn_time.day <= 5 else 0

        # Device change
        usual_dev = cust_device.get(cust_id, "Android")
        device_change = 1 if txn["device_type"] != usual_dev else 0

        # Location change
        usual_city = cust_city.get(cust_id, "Mumbai")
        location_change = 1 if txn["device_location"] != usual_city else 0

        # Monthly spending ratio
        monthly_spend = cust_avg_spend.get(cust_id, 30000)
        monthly_spending_ratio = round(amount / max(monthly_spend, 1), 4)

        # Transfer ratio (amount / avg transfer)
        avg_transfer = cust_avg_txn.get(cust_id, 5000)
        avg_transfer_ratio = round(amount / max(avg_transfer, 1), 4)

        # Transaction velocity (time since last transaction for this customer)
        if cust_id == prev_cust and prev_time is not None:
            time_since_last = max((txn_time - prev_time).total_seconds() / 3600, 0.01)  # hours
        else:
            time_since_last = 24.0  # default

        # Behavior score (composite of normalcy indicators)
        behavior_score = round(10.0
                               - abs(amount_deviation) * 2
                               - night_txn * 2
                               - device_change * 3
                               - location_change * 2
                               - new_recipient * 3
                               + is_trusted * 2, 2)
        behavior_score = round(np.clip(behavior_score, 0, 10), 2)

        # Merchant trust
        merchant_trust = mer_trust.get(mer_id, 0.8) if pd.notna(mer_id) else 0.8
        merchant_risk = 1 if mer_risk.get(mer_id, "Low") == "High" else 0

        # Customer risk profile numeric
        risk_prof = cust_risk_prof.get(cust_id, "Moderate")
        risk_prof_num = {"Conservative": 0, "Moderate": 1, "Aggressive": 2}.get(risk_prof, 1)

        # Recipient risk score
        rec_first = rec_first_added.get(rec_id) if pd.notna(rec_id) else None
        if rec_first:
            try:
                days_known = (txn_time - pd.to_datetime(rec_first)).days
            except Exception:
                days_known = 365
        else:
            days_known = 0
        recipient_risk_score = round(np.clip(
            (1 - is_trusted) * 0.3 +
            (new_recipient) * 0.3 +
            max(0, (1 - days_known / 365)) * 0.2 +
            max(0, (1 - rec_freq / 20)) * 0.2,
            0, 1
        ), 3)

        # Label: is this a risky transaction?
        is_risky = txn["transaction_id"] in risk_txn_set
        risk_label = 1 if is_risky and risk_levels.get(txn["transaction_id"], "Low") in ("High", "Critical") else 0
        fraud_confirmed = 1 if risk_outcomes.get(txn["transaction_id"]) == "Fraud Confirmed" else 0

        features.append({
            "transaction_id": txn["transaction_id"],
            "customer_id": cust_id,
            "amount": amount,
            "amount_deviation": amount_deviation,
            "recipient_frequency": rec_freq,
            "new_recipient": new_recipient,
            "night_transaction": night_txn,
            "device_change": device_change,
            "location_change": location_change,
            "average_transfer_ratio": avg_transfer_ratio,
            "monthly_spending_ratio": monthly_spending_ratio,
            "transaction_velocity": round(time_since_last, 2),
            "behavior_score": behavior_score,
            "merchant_trust_score": float(merchant_trust),
            "customer_risk_profile": risk_prof_num,
            "holiday_transaction": holiday_txn,
            "weekend_transaction": weekend_txn,
            "salary_week": salary_week,
            "recipient_risk_score": recipient_risk_score,
            "time_since_last_transaction": round(time_since_last, 2),
            "hour": hour,
            "credit_score": cust_credit.get(cust_id, 700),
            "is_trusted_recipient": int(is_trusted),
            "risk_label": risk_label,
            "fraud_confirmed": fraud_confirmed,
        })

        prev_cust = cust_id
        prev_time = txn_time

    return pd.DataFrame(features)
