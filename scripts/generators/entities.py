"""
NIRNAY — Core Entity Generators
================================
Generates: customers.csv, accounts.csv, recipients.csv,
           merchants.csv, merchant_reputation.csv

All entities maintain referential integrity through ID-based foreign keys.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


def _weighted_choice(rng, options, weights):
    """Pick from options with given weights (auto-normalizes)."""
    w = np.array(weights, dtype=float)
    w /= w.sum()
    return options[rng.choice(len(options), p=w)]


def _weighted_choice_dict(rng, dicts, weight_key="weight"):
    """Pick a dict from a list of dicts using a weight field."""
    weights = np.array([d[weight_key] for d in dicts], dtype=float)
    weights /= weights.sum()
    idx = rng.choice(len(dicts), p=weights)
    return dicts[idx]


# ──────────────────────────────────────────────────────────────────────
# CUSTOMERS
# ──────────────────────────────────────────────────────────────────────
def generate_customers(rng, n=NUM_CUSTOMERS):
    """Generate n realistic Indian banking customers."""
    records = []
    for i in range(n):
        gender = rng.choice(["Male", "Female"], p=[0.55, 0.45])
        first_names = MALE_FIRST_NAMES if gender == "Male" else FEMALE_FIRST_NAMES
        first_name = rng.choice(first_names)
        last_name = rng.choice(LAST_NAMES)
        full_name = f"{first_name} {last_name}"

        # Age: bell-curve centered at 34 for digital banking users
        age = int(np.clip(rng.normal(34, 11), 18, 75))
        dob_year = 2026 - age
        dob_month = rng.integers(1, 13)
        dob_day = rng.integers(1, 29)  # safe for all months
        dob = f"{dob_year}-{dob_month:02d}-{dob_day:02d}"

        # Location
        city_info = _weighted_choice_dict(rng, CITIES, "lat")  # hack — use idx
        city_idx = rng.choice(len(CITIES), p=np.array(CITY_WEIGHTS) / sum(CITY_WEIGHTS))
        city_info = CITIES[city_idx]
        pincode = f"{city_info['pin']}{rng.integers(1, 100):03d}"

        # Occupation & income
        occ = _weighted_choice_dict(rng, OCCUPATIONS)
        annual_income = int(rng.uniform(occ["min"], occ["max"]))
        # Students and homemakers get lower but non-zero income
        if occ["type"] in ("Student", "Homemaker") and annual_income == 0:
            annual_income = int(rng.uniform(0, occ["max"]))
        monthly_income = annual_income // 12

        # Credit score correlated with income & age
        base_credit = 500 + (annual_income / 100000) * 25 + age * 1.5
        credit_score = int(np.clip(rng.normal(base_credit, 50), 300, 900))

        # Spending patterns correlated with income
        spending_ratio = rng.uniform(0.30, 0.70)
        avg_monthly_spending = max(int(monthly_income * spending_ratio), 2000)
        avg_transfer_amount = max(int(avg_monthly_spending * rng.uniform(0.10, 0.40)), 500)
        avg_balance = max(int(monthly_income * rng.uniform(1.0, 5.0)), 5000)

        # Customer since
        cs_start = datetime(2016, 1, 1)
        cs_end = datetime(2025, 12, 31)
        cs_days = (cs_end - cs_start).days
        customer_since = cs_start + timedelta(days=int(rng.integers(0, cs_days)))

        # Device
        device_type = _weighted_choice(rng, DEVICE_TYPES, DEVICE_WEIGHTS)
        device_id = f"DEV{i+1:06d}{rng.integers(1000, 9999)}"

        # Preferred transaction time (hour)
        pref_hour = int(np.clip(rng.normal(14, 4), 6, 23))

        records.append({
            "customer_id": f"CUS{i+1:06d}",
            "full_name": full_name,
            "gender": gender,
            "age": age,
            "dob": dob,
            "occupation": occ["title"],
            "employment_type": occ["type"],
            "annual_income": annual_income,
            "monthly_income": monthly_income,
            "city": city_info["city"],
            "state": city_info["state"],
            "country": "India",
            "pincode": pincode,
            "customer_since": customer_since.strftime("%Y-%m-%d"),
            "account_type": _weighted_choice(rng, ACCOUNT_TYPES, ACCOUNT_TYPE_WEIGHTS),
            "risk_profile": _weighted_choice(rng, RISK_PROFILES, RISK_PROFILE_WEIGHTS),
            "kyc_status": _weighted_choice(rng, KYC_STATUS, KYC_WEIGHTS),
            "marital_status": _weighted_choice(rng, MARITAL_STATUS, MARITAL_WEIGHTS),
            "education": _weighted_choice(rng, EDUCATION_LEVELS, EDUCATION_WEIGHTS),
            "preferred_language": _weighted_choice(rng, LANGUAGES, LANGUAGE_WEIGHTS),
            "preferred_transaction_time": f"{pref_hour:02d}:00",
            "credit_score": credit_score,
            "average_monthly_spending": avg_monthly_spending,
            "average_transfer_amount": avg_transfer_amount,
            "average_balance": avg_balance,
            "registered_device_id": device_id,
            "device_type": device_type,
            "email": f"{first_name.lower()}.{last_name.lower()}{rng.integers(1, 999)}@{'gmail.com' if rng.random() < 0.7 else 'outlook.com'}",
            "phone": f"+91{rng.integers(70000, 99999)}{rng.integers(10000, 99999)}",
        })

    return pd.DataFrame(records)


# ──────────────────────────────────────────────────────────────────────
# ACCOUNTS
# ──────────────────────────────────────────────────────────────────────
def generate_accounts(rng, customers_df):
    """Generate one bank account per customer (with ~10% having a second)."""
    records = []
    acc_counter = 0

    for _, cust in customers_df.iterrows():
        num_accounts = 1 if rng.random() < 0.90 else 2
        for j in range(num_accounts):
            acc_counter += 1
            bank_idx = rng.choice(len(BANKS), p=np.array(BANK_WEIGHTS) / sum(BANK_WEIGHTS))
            bank = BANKS[bank_idx]

            # Balance correlated with customer income
            base_balance = cust["average_balance"]
            current_balance = max(round(rng.normal(base_balance, base_balance * 0.3), 2), 1000)
            available_balance = round(current_balance * rng.uniform(0.85, 1.0), 2)

            # Account opened within the customer_since range
            cs = datetime.strptime(cust["customer_since"], "%Y-%m-%d")
            opened_offset = timedelta(days=int(rng.integers(0, max((datetime(2026, 6, 30) - cs).days, 1))))
            opened_date = cs + timedelta(days=min(opened_offset.days, 365 * 2))

            acct_type = cust["account_type"] if j == 0 else rng.choice(["Savings", "Current"])

            records.append({
                "account_id": f"ACC{acc_counter:06d}",
                "customer_id": cust["customer_id"],
                "bank_name": bank["name"],
                "branch": f"{cust['city']} Main Branch" if j == 0 else f"{cust['city']} Branch {rng.integers(2, 10)}",
                "account_number": f"{rng.integers(10000000, 99999999)}{rng.integers(1000, 9999)}",
                "ifsc": f"{bank['ifsc']}{rng.integers(100000, 999999)}",
                "account_type": acct_type,
                "current_balance": current_balance,
                "available_balance": available_balance,
                "account_status": "Active" if rng.random() < 0.95 else rng.choice(["Dormant", "Frozen"]),
                "opened_date": opened_date.strftime("%Y-%m-%d"),
            })

    return pd.DataFrame(records)


# ──────────────────────────────────────────────────────────────────────
# RECIPIENTS
# ──────────────────────────────────────────────────────────────────────
def generate_recipients(rng, customers_df):
    """Generate 3-12 recipients per customer, maintaining realistic distributions."""
    records = []
    rec_counter = 0

    for _, cust in customers_df.iterrows():
        n_recipients = rng.integers(RECIPIENTS_PER_CUSTOMER[0], RECIPIENTS_PER_CUSTOMER[1] + 1)
        for _ in range(n_recipients):
            rec_counter += 1
            relationship = _weighted_choice(rng, RELATIONSHIP_TYPES, RELATIONSHIP_WEIGHTS)

            # Generate recipient name based on relationship
            if relationship == "Merchant":
                cat = rng.choice(MERCHANT_CATEGORIES)
                names_list = MERCHANT_NAMES_BY_CATEGORY.get(cat, ["Local Shop"])
                rec_name = rng.choice(names_list)
            else:
                r_gender = rng.choice(["Male", "Female"])
                r_first = rng.choice(MALE_FIRST_NAMES if r_gender == "Male" else FEMALE_FIRST_NAMES)
                r_last = rng.choice(LAST_NAMES)
                rec_name = f"{r_first} {r_last}"

            bank_idx = rng.choice(len(BANKS), p=np.array(BANK_WEIGHTS) / sum(BANK_WEIGHTS))
            bank = BANKS[bank_idx]

            # Trusted recipients are mostly family/friends with history
            is_trusted = (relationship in ["Family", "Friend"] and rng.random() < 0.7) or \
                         (relationship == "Colleague" and rng.random() < 0.3)

            txn_count = int(rng.exponential(8)) + 1 if is_trusted else int(rng.exponential(3)) + 1

            first_added = datetime.strptime(cust["customer_since"], "%Y-%m-%d") + \
                          timedelta(days=int(rng.integers(0, 365 * 3)))
            if first_added > datetime(2026, 6, 30):
                first_added = datetime(2026, 6, 30) - timedelta(days=int(rng.integers(30, 365)))

            last_txn = first_added + timedelta(days=int(rng.integers(1, max((datetime(2026, 6, 30) - first_added).days, 2))))
            if last_txn > datetime(2026, 6, 30):
                last_txn = datetime(2026, 6, 30)

            rec_type = _weighted_choice(rng, RECIPIENT_TYPES, RECIPIENT_TYPE_WEIGHTS)
            if relationship == "Merchant":
                rec_type = "Merchant"
            elif relationship == "Business":
                rec_type = "Business"

            records.append({
                "recipient_id": f"REC{rec_counter:06d}",
                "customer_id": cust["customer_id"],
                "recipient_name": rec_name,
                "recipient_bank": bank["name"],
                "recipient_account_number": f"{rng.integers(10000000, 99999999)}{rng.integers(1000, 9999)}",
                "recipient_ifsc": f"{bank['ifsc']}{rng.integers(100000, 999999)}",
                "recipient_type": rec_type,
                "relationship": relationship,
                "trusted_recipient": is_trusted,
                "first_added": first_added.strftime("%Y-%m-%d"),
                "last_transaction_date": last_txn.strftime("%Y-%m-%d"),
                "transaction_count": txn_count,
            })

    return pd.DataFrame(records)


# ──────────────────────────────────────────────────────────────────────
# MERCHANTS
# ──────────────────────────────────────────────────────────────────────
def generate_merchants(rng, n=NUM_MERCHANTS):
    """Generate n realistic Indian merchants with trust/risk profiles."""
    records = []
    used_names = set()
    merchant_counter = 0

    for cat in MERCHANT_CATEGORIES:
        names = MERCHANT_NAMES_BY_CATEGORY.get(cat, [])
        for name in names:
            if name not in used_names and merchant_counter < n:
                merchant_counter += 1
                used_names.add(name)

                city_idx = rng.choice(len(CITIES), p=np.array(CITY_WEIGHTS) / sum(CITY_WEIGHTS))
                city_info = CITIES[city_idx]

                risk_level = _weighted_choice(rng, MERCHANT_RISK_LEVELS, MERCHANT_RISK_WEIGHTS)
                trust_score = round(rng.uniform(0.7, 1.0) if risk_level == "Low" else
                                    rng.uniform(0.4, 0.7) if risk_level == "Medium" else
                                    rng.uniform(0.1, 0.4), 2)
                verified = risk_level != "High" and rng.random() < 0.85
                scam_count = 0 if risk_level == "Low" else \
                             rng.integers(1, 5) if risk_level == "Medium" else \
                             rng.integers(3, 20)

                records.append({
                    "merchant_id": f"MER{merchant_counter:06d}",
                    "merchant_name": name,
                    "merchant_category": cat,
                    "merchant_city": city_info["city"],
                    "merchant_state": city_info["state"],
                    "merchant_country": "India",
                    "trust_score": trust_score,
                    "verified": verified,
                    "registration_status": "Registered" if verified else rng.choice(["Pending", "Unregistered"]),
                    "merchant_risk_level": risk_level,
                    "reported_scam_count": scam_count,
                })

    # Fill remaining slots with generic local merchants
    while merchant_counter < n:
        merchant_counter += 1
        cat = rng.choice(MERCHANT_CATEGORIES)
        city_idx = rng.choice(len(CITIES), p=np.array(CITY_WEIGHTS) / sum(CITY_WEIGHTS))
        city_info = CITIES[city_idx]
        name = f"Local {cat} #{merchant_counter}"

        risk_level = _weighted_choice(rng, MERCHANT_RISK_LEVELS, MERCHANT_RISK_WEIGHTS)
        trust_score = round(rng.uniform(0.5, 1.0) if risk_level == "Low" else
                            rng.uniform(0.3, 0.6) if risk_level == "Medium" else
                            rng.uniform(0.05, 0.3), 2)

        records.append({
            "merchant_id": f"MER{merchant_counter:06d}",
            "merchant_name": name,
            "merchant_category": cat,
            "merchant_city": city_info["city"],
            "merchant_state": city_info["state"],
            "merchant_country": "India",
            "trust_score": trust_score,
            "verified": risk_level == "Low" and rng.random() < 0.7,
            "registration_status": rng.choice(["Registered", "Pending", "Unregistered"], p=[0.6, 0.2, 0.2]),
            "merchant_risk_level": risk_level,
            "reported_scam_count": 0 if risk_level == "Low" else rng.integers(1, 10),
        })

    return pd.DataFrame(records)


# ──────────────────────────────────────────────────────────────────────
# MERCHANT REPUTATION (derived from merchants)
# ──────────────────────────────────────────────────────────────────────
def generate_merchant_reputation(rng, merchants_df):
    """Generate merchant_reputation.csv from merchant base data."""
    records = []
    for _, m in merchants_df.iterrows():
        records.append({
            "merchant_id": m["merchant_id"],
            "merchant_name": m["merchant_name"],
            "trust_score": m["trust_score"],
            "verified": m["verified"],
            "government_registered": m["registration_status"] == "Registered",
            "reported_scam_count": m["reported_scam_count"],
            "risk_level": m["merchant_risk_level"],
            "last_updated": (datetime(2026, 6, 30) - timedelta(days=int(rng.integers(0, 90)))).strftime("%Y-%m-%d"),
        })
    return pd.DataFrame(records)
