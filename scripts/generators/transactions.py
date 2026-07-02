"""
NIRNAY — Transaction Generator
===============================
Generates: transactions.csv (50,000+ realistic banking transactions)

95% legitimate transactions with realistic distributions.
5% suspicious/scam-related transactions for ML training.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


def _weighted_choice(rng, options, weights):
    w = np.array(weights, dtype=float)
    w /= w.sum()
    return options[rng.choice(len(options), p=w)]


def generate_transactions(rng, customers_df, accounts_df, recipients_df, merchants_df,
                          n=NUM_TRANSACTIONS):
    """
    Generate n realistic banking transactions.

    Distribution logic:
    - Each customer gets a proportional share of transactions based on their
      spending pattern (higher income = more transactions).
    - 95% legitimate with realistic category/amount distributions.
    - 5% suspicious/scam-related with elevated amounts and red-flag indicators.
    """
    records = []

    # Pre-compute customer lookup structures
    cust_ids = customers_df["customer_id"].values
    n_cust = len(cust_ids)

    # Account lookup: customer_id → first account_id
    acct_map = accounts_df.groupby("customer_id")["account_id"].first().to_dict()

    # Recipient lookup: customer_id → list of recipient_ids
    rec_map = recipients_df.groupby("customer_id")["recipient_id"].apply(list).to_dict()

    # Merchant IDs
    merchant_ids = merchants_df["merchant_id"].values
    merchant_names = merchants_df["merchant_name"].values
    merchant_cats = merchants_df["merchant_category"].values

    # Customer income for amount scaling
    income_map = dict(zip(customers_df["customer_id"], customers_df["monthly_income"]))
    city_map = dict(zip(customers_df["customer_id"], customers_df["city"]))
    device_map = dict(zip(customers_df["customer_id"], customers_df["device_type"]))

    # Category weights
    cat_names = list(TRANSACTION_CATEGORIES.keys())
    cat_weights = np.array([TRANSACTION_CATEGORIES[c]["weight"] for c in cat_names])
    cat_weights /= cat_weights.sum()

    # Date range for transactions
    start_dt = datetime.strptime(DATA_START_DATE, "%Y-%m-%d")
    end_dt = datetime.strptime(DATA_END_DATE, "%Y-%m-%d")
    date_range_days = (end_dt - start_dt).days

    # Assign transaction counts per customer (proportional to income)
    incomes = customers_df["monthly_income"].values.astype(float)
    income_weights = np.clip(incomes, 5000, None)  # minimum weight
    income_weights = income_weights / income_weights.sum()
    txn_per_customer = rng.multinomial(n, income_weights)

    # Determine which transactions are suspicious
    n_suspicious = int(n * SUSPICIOUS_RATIO)
    suspicious_indices = set(rng.choice(n, size=n_suspicious, replace=False))

    txn_counter = 0
    global_idx = 0

    for cust_idx in range(n_cust):
        cust_id = cust_ids[cust_idx]
        cust_txn_count = txn_per_customer[cust_idx]
        monthly_income = income_map.get(cust_id, 30000)
        acct_id = acct_map.get(cust_id, f"ACC{cust_idx+1:06d}")
        cust_recipients = rec_map.get(cust_id, [])
        cust_city = city_map.get(cust_id, "Mumbai")
        cust_device = device_map.get(cust_id, "Android")

        # Find city lat/lon
        city_info = next((c for c in CITIES if c["city"] == cust_city), CITIES[0])

        for _ in range(cust_txn_count):
            txn_counter += 1
            is_suspicious = global_idx in suspicious_indices
            global_idx += 1

            # ── Timestamp ──────────────────────────────────────────
            # Realistic: more transactions during business hours (9-18),
            # fewer late night (23-5)
            txn_date = start_dt + timedelta(days=int(rng.integers(0, date_range_days)))
            if is_suspicious and rng.random() < 0.3:
                # Suspicious transactions more likely at unusual hours
                hour = rng.choice([0, 1, 2, 3, 4, 23], p=[0.15, 0.2, 0.2, 0.2, 0.15, 0.1])
            else:
                # Normal hour distribution: peak at 10-14, taper off
                hour = int(np.clip(rng.normal(13, 4), 0, 23))
            minute = rng.integers(0, 60)
            second = rng.integers(0, 60)
            timestamp = txn_date.replace(hour=hour, minute=minute, second=second)

            # ── Category & Amount ──────────────────────────────────
            if is_suspicious:
                # Suspicious transactions are often Investment, Transfer
                sus_cats = ["Investment", "Transfer"]
                category = rng.choice(sus_cats) if rng.random() < 0.6 else \
                           cat_names[rng.choice(len(cat_names), p=cat_weights)]

                # Higher amounts for scams
                cat_cfg = TRANSACTION_CATEGORIES.get(category, TRANSACTION_CATEGORIES["Transfer"])
                base_amount = max(monthly_income * rng.uniform(0.3, 2.0), cat_cfg["min"])
                amount = round(min(base_amount, cat_cfg["max"] * 3), 2)

                # Scam amounts often round numbers
                if rng.random() < 0.5:
                    amount = round(amount / 1000) * 1000
                    amount = max(amount, 5000)
            else:
                category = cat_names[rng.choice(len(cat_names), p=cat_weights)]
                cat_cfg = TRANSACTION_CATEGORIES[category]

                # Amount from truncated normal distribution, scaled by income
                income_factor = max(monthly_income / 50000, 0.3)  # scale relative to median
                raw_amount = abs(rng.normal(cat_cfg["mean"] * income_factor,
                                           cat_cfg["std"] * income_factor))
                amount = round(np.clip(raw_amount, cat_cfg["min"], cat_cfg["max"]), 2)

                # Salary is exactly monthly income
                if category == "Salary":
                    amount = monthly_income + round(rng.normal(0, monthly_income * 0.05), 2)
                    amount = max(amount, 10000)

            # ── Transaction Type & Channel ─────────────────────────
            if category in ("Salary",):
                txn_type = "Credit"
            elif category in ("Investment", "Insurance", "EMI"):
                txn_type = "Debit"
            else:
                txn_type = "Debit" if rng.random() < 0.85 else "Credit"

            # Channel depends on amount
            if amount >= 200000:
                channel = "RTGS"
            elif amount >= 50000 and rng.random() < 0.4:
                channel = "NEFT"
            else:
                channel = _weighted_choice(rng, PAYMENT_CHANNELS, PAYMENT_CHANNEL_WEIGHTS)

            # ── Recipient & Merchant ───────────────────────────────
            recipient_id = None
            merchant_id = None
            merchant_name_val = None

            if category in ("Shopping", "Food & Dining", "Fuel", "Entertainment",
                            "Subscription", "Healthcare"):
                # Merchant transaction
                cat_merchants = np.where(merchant_cats == category)[0] if category in MERCHANT_TO_TXN_CATEGORY.values() else []
                # Find merchants whose category maps to this txn category
                matching_idx = [i for i, mc in enumerate(merchant_cats)
                                if MERCHANT_TO_TXN_CATEGORY.get(mc) == category]
                if matching_idx:
                    m_idx = rng.choice(matching_idx)
                else:
                    m_idx = rng.integers(0, len(merchant_ids))
                merchant_id = merchant_ids[m_idx]
                merchant_name_val = merchant_names[m_idx]

                # Also pick a recipient (the merchant as recipient)
                if cust_recipients:
                    recipient_id = rng.choice(cust_recipients)
            else:
                # Person-to-person or self transfer
                if cust_recipients:
                    if is_suspicious and rng.random() < 0.7:
                        # Suspicious: prefer unknown/new recipients
                        cust_recs_df = recipients_df[recipients_df["customer_id"] == cust_id]
                        unknown_recs = cust_recs_df[
                            cust_recs_df["relationship"].isin(["Unknown", "Business"])
                        ]["recipient_id"].values
                        if len(unknown_recs) > 0:
                            recipient_id = rng.choice(unknown_recs)
                        else:
                            recipient_id = rng.choice(cust_recipients)
                    else:
                        recipient_id = rng.choice(cust_recipients)

            # ── Device & Location ──────────────────────────────────
            if is_suspicious and rng.random() < 0.2:
                device = rng.choice(DEVICE_TYPES)  # unusual device
            else:
                device = cust_device

            # Location jitter (small variation around city center)
            lat = round(city_info["lat"] + rng.normal(0, 0.05), 6)
            lon = round(city_info["lon"] + rng.normal(0, 0.05), 6)

            if is_suspicious and rng.random() < 0.15:
                # Location anomaly — different city
                other_city = CITIES[rng.integers(0, len(CITIES))]
                lat = round(other_city["lat"] + rng.normal(0, 0.03), 6)
                lon = round(other_city["lon"] + rng.normal(0, 0.03), 6)
                device_location = other_city["city"]
            else:
                device_location = cust_city

            # ── Status ─────────────────────────────────────────────
            status = _weighted_choice(rng, TRANSACTION_STATUSES, TRANSACTION_STATUS_WEIGHTS)
            if is_suspicious and rng.random() < 0.15:
                status = rng.choice(["Cancelled", "Reversed", "Pending"])

            # ── Remarks ────────────────────────────────────────────
            if is_suspicious and rng.random() < 0.6:
                remark_template = rng.choice(SCAM_REMARKS)
                remark = remark_template.format(
                    pct=rng.integers(20, 100),
                    amount=int(amount * rng.uniform(5, 20))
                )
            else:
                cat_remarks = NORMAL_REMARKS.get(category, NORMAL_REMARKS["Transfer"])
                remark = rng.choice(cat_remarks)

            # ── Day features ───────────────────────────────────────
            day_of_week = timestamp.strftime("%A")
            hour_val = timestamp.hour

            records.append({
                "transaction_id": f"TXN{txn_counter:07d}",
                "customer_id": cust_id,
                "account_id": acct_id,
                "recipient_id": recipient_id,
                "merchant_id": merchant_id,
                "transaction_type": txn_type,
                "payment_channel": channel,
                "category": category,
                "merchant_name": merchant_name_val,
                "amount": amount,
                "currency": "INR",
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "day_of_week": day_of_week,
                "hour": hour_val,
                "device_type": device,
                "device_location": device_location,
                "geo_latitude": lat,
                "geo_longitude": lon,
                "transaction_status": status,
                "remarks": remark,
            })

    return pd.DataFrame(records)
