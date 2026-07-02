"""
NIRNAY — Risk Intelligence Generators
======================================
Generates: scam_patterns.csv, risk_events.csv,
           conversations.csv, feedback.csv

These datasets power the Decision Intelligence layer and agentic AI.
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


# ──────────────────────────────────────────────────────────────────────
# SCAM PATTERNS (200+)
# ──────────────────────────────────────────────────────────────────────
def generate_scam_patterns(rng):
    """Generate 200+ scam patterns from templates with variations."""
    records = []
    pattern_counter = 0

    recommended_actions = {
        "Low": "Monitor transaction",
        "Medium": "Show warning to customer",
        "High": "Initiate agentic conversation",
        "Critical": "Block transaction automatically",
    }

    agent_responses = {
        "Investment Scam": "I notice this transaction matches patterns commonly associated with investment scams. No legitimate investment guarantees fixed returns. Have you independently verified this opportunity?",
        "Impersonation Scam": "This request appears to impersonate an authority figure. Legitimate banks and government agencies never ask for payments through personal accounts or phone calls.",
        "Romance Scam": "I've noticed some concerning patterns in this transaction. Online relationships that quickly escalate to financial requests are a common scam tactic. Have you met this person in real life?",
        "Tech Support Scam": "Legitimate technology companies do not make unsolicited calls about viruses or security issues. This appears to follow a known tech support scam pattern.",
        "Lottery Scam": "You cannot win a lottery you didn't enter. Legitimate prizes never require upfront payment. This follows a known lottery scam pattern.",
        "Advance Fee Scam": "Legitimate services don't require upfront fees through informal channels. This matches a known advance fee fraud pattern.",
        "Crypto Scam": "No legitimate cryptocurrency platform guarantees returns. This matches patterns of known crypto investment fraud schemes.",
        "Deepfake Scam": "We've detected indicators consistent with deepfake-assisted fraud. Please verify the identity of the person you spoke with through an independent channel.",
        "Emergency Scam": "Scammers create false urgency using emergency situations. Please independently verify this emergency before transferring any funds.",
        "Money Mule": "This transaction pattern suggests your account may be used to move funds for criminal activity. Please reconsider this transfer.",
        "Fake Bank Officer": "Banks never ask customers to transfer money to secure their accounts. This is a known impersonation tactic. Please call your bank directly.",
        "Job Scam": "Legitimate employers never ask for payment as part of the hiring process. This matches a known employment scam pattern.",
        "Charity Scam": "Please verify this charity through official government databases before donating. Scammers exploit emotions around disasters and social causes.",
        "Phishing": "This transaction appears to have originated from a phishing link. Please verify the website URL and never share OTPs or passwords.",
    }

    customer_responses_safe = [
        "Thank you for the warning. I will cancel this transaction.",
        "I didn't realize this was a scam. I will not proceed.",
        "I appreciate the alert. Let me verify this independently first.",
    ]
    customer_responses_risky = [
        "I know this person, I want to proceed anyway.",
        "This is a legitimate investment, I have done my research.",
        "I understand the risk but I still want to continue.",
    ]

    for category, templates in SCAM_TEMPLATES.items():
        for template in templates:
            pattern_counter += 1
            severity = rng.choice(["Medium", "High", "Critical"], p=[0.3, 0.5, 0.2])
            if "Critical" in category or "Deepfake" in category:
                severity = rng.choice(["High", "Critical"], p=[0.4, 0.6])

            desc = template["desc"].format(
                pct=rng.integers(10, 80),
                amount=rng.integers(50000, 500000)
            ) if "{pct}" in template["desc"] or "{amount}" in template["desc"] else template["desc"]

            records.append({
                "pattern_id": f"PAT{pattern_counter:04d}",
                "pattern_name": template["name"],
                "category": category,
                "description": desc,
                "behavior_signature": template["sig"],
                "risk_level": severity,
                "recommended_action": recommended_actions[severity],
                "expected_agent_response": agent_responses.get(category, agent_responses["Phishing"]),
                "expected_customer_response": rng.choice(
                    customer_responses_safe if rng.random() < 0.6 else customer_responses_risky
                ),
            })

    # Pad to reach NUM_SCAM_PATTERNS if needed
    base_cats = list(SCAM_TEMPLATES.keys())
    while pattern_counter < NUM_SCAM_PATTERNS:
        pattern_counter += 1
        cat = rng.choice(base_cats)
        severity = rng.choice(["Medium", "High", "Critical"], p=[0.3, 0.5, 0.2])
        records.append({
            "pattern_id": f"PAT{pattern_counter:04d}",
            "pattern_name": f"{cat} Variant #{pattern_counter}",
            "category": cat,
            "description": f"Variant of {cat.lower()} using alternative social engineering techniques and communication channels.",
            "behavior_signature": "variant_pattern|social_engineering|alternate_channel",
            "risk_level": severity,
            "recommended_action": recommended_actions[severity],
            "expected_agent_response": agent_responses.get(cat, agent_responses["Phishing"]),
            "expected_customer_response": rng.choice(customer_responses_safe),
        })

    return pd.DataFrame(records)


# ──────────────────────────────────────────────────────────────────────
# RISK EVENTS
# ──────────────────────────────────────────────────────────────────────
def generate_risk_events(rng, transactions_df, customers_df, recipients_df, scam_patterns_df):
    """
    Generate risk events for suspicious and borderline transactions.
    ~5% of transactions trigger risk events.
    """
    records = []
    event_counter = 0

    # Identify suspicious transactions (those with scam-like remarks or high amounts)
    txn_df = transactions_df.copy()

    # Customer income lookup
    income_map = dict(zip(customers_df["customer_id"], customers_df["monthly_income"]))
    avg_txn_map = dict(zip(customers_df["customer_id"], customers_df["average_transfer_amount"]))

    # Recipient trust lookup
    trust_map = dict(zip(recipients_df["recipient_id"], recipients_df["trusted_recipient"]))
    rel_map = dict(zip(recipients_df["recipient_id"], recipients_df["relationship"]))

    # Pattern IDs for matching
    pattern_ids = scam_patterns_df["pattern_id"].values
    pattern_cats = scam_patterns_df["category"].values

    # Score each transaction for risk
    for idx, txn in txn_df.iterrows():
        cust_id = txn["customer_id"]
        monthly_income = income_map.get(cust_id, 30000)
        avg_txn_amt = avg_txn_map.get(cust_id, 5000)
        is_trusted = trust_map.get(txn.get("recipient_id"), False) if pd.notna(txn.get("recipient_id")) else False
        relationship = rel_map.get(txn.get("recipient_id"), "Unknown") if pd.notna(txn.get("recipient_id")) else "Unknown"

        # ── Calculate risk signals ─────────────────────────────────
        amount = txn["amount"]
        hour = txn["hour"]
        risk_score = 0.0
        triggers = []

        # Amount deviation
        if avg_txn_amt > 0:
            amount_ratio = amount / avg_txn_amt
            if amount_ratio > 5:
                risk_score += 25
                triggers.append("Large Amount")
            elif amount_ratio > 3:
                risk_score += 15
                triggers.append("Large Amount")

        # New / untrusted recipient
        if not is_trusted and relationship in ("Unknown", "Business"):
            risk_score += 15
            triggers.append("New Recipient")

        # Late night transaction
        if hour >= 23 or hour <= 4:
            risk_score += 10
            triggers.append("Late Night")

        # Scam-like remarks
        remarks = str(txn.get("remarks", "")).lower()
        scam_keywords = ["guaranteed", "double", "lottery", "prize", "urgent",
                         "blocked", "freeze", "processing fee", "arrest",
                         "crypto", "investment scheme", "returns"]
        keyword_matches = sum(1 for kw in scam_keywords if kw in remarks)
        if keyword_matches >= 2:
            risk_score += 30
            triggers.append("Investment Scam" if "investment" in remarks or "returns" in remarks
                           else "Impersonation Scam" if "blocked" in remarks or "freeze" in remarks
                           else "Lottery Scam" if "lottery" in remarks or "prize" in remarks
                           else "Crypto Scam" if "crypto" in remarks
                           else "Behavior Deviation")
        elif keyword_matches == 1:
            risk_score += 12
            triggers.append("Behavior Deviation")

        # Category-based risk
        if txn["category"] == "Investment" and amount > 20000:
            risk_score += 10
        if txn["category"] == "Transfer" and amount > 50000 and not is_trusted:
            risk_score += 12

        # Add noise
        risk_score += rng.normal(0, 5)
        risk_score = round(np.clip(risk_score, 0, 100), 1)

        # Only create risk event if score is meaningful (> 20)
        if risk_score < 20:
            continue

        event_counter += 1

        # Determine risk level
        if risk_score <= 30:
            risk_level = "Low"
        elif risk_score <= 50:
            risk_level = "Medium"
        elif risk_score <= 90:
            risk_level = "High"
        else:
            risk_level = "Critical"

        # Risk type — primary trigger
        risk_type = triggers[0] if triggers else "Behavior Deviation"

        # ML probability (calibrated probability from model)
        ml_prob = round(np.clip(risk_score / 100 + rng.normal(0, 0.05), 0.01, 0.99), 3)

        # Agent decision
        if risk_level == "Low":
            agent_decision = "Approve"
        elif risk_level == "Medium":
            agent_decision = rng.choice(["Warn", "Approve"], p=[0.7, 0.3])
        elif risk_level == "High":
            agent_decision = rng.choice(["Warn", "Block", "Escalate"], p=[0.4, 0.3, 0.3])
        else:
            agent_decision = rng.choice(["Block", "Escalate"], p=[0.7, 0.3])

        # Customer response
        if risk_level in ("High", "Critical"):
            customer_response = rng.choice(
                ["Cancelled", "Proceeded Anyway", "Verified and Proceeded", "Reported Scam"],
                p=[0.4, 0.2, 0.2, 0.2]
            )
        elif risk_level == "Medium":
            customer_response = rng.choice(
                ["Proceeded", "Cancelled", "Verified and Proceeded"],
                p=[0.5, 0.3, 0.2]
            )
        else:
            customer_response = "Proceeded"

        # Final outcome
        if customer_response == "Cancelled" or agent_decision == "Block":
            final_outcome = "Prevented"
        elif customer_response == "Reported Scam":
            final_outcome = "Fraud Confirmed"
        elif risk_level in ("High", "Critical") and customer_response == "Proceeded Anyway":
            final_outcome = rng.choice(["Fraud Confirmed", "False Alarm"], p=[0.6, 0.4])
        else:
            final_outcome = rng.choice(["Safe", "False Alarm", "Under Review"], p=[0.6, 0.3, 0.1])

        # Explanation
        trigger_str = ", ".join(triggers[:3])
        explanation = (
            f"Risk score {risk_score:.1f}/100. Triggered by: {trigger_str}. "
            f"Transaction of INR {amount:,.2f} to {'untrusted' if not is_trusted else 'trusted'} "
            f"recipient via {txn['payment_channel']} at {hour:02d}:00."
        )

        # Match to scam pattern
        matched_pattern = None
        for t in triggers:
            matching = [i for i, pc in enumerate(pattern_cats) if t in pc]
            if matching:
                matched_pattern = pattern_ids[rng.choice(matching)]
                break

        confidence = round(np.clip(ml_prob + rng.uniform(-0.1, 0.1), 0.1, 0.99), 2)

        records.append({
            "risk_event_id": f"RSK{event_counter:06d}",
            "transaction_id": txn["transaction_id"],
            "customer_id": cust_id,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_type": risk_type,
            "trigger_reason": trigger_str,
            "ml_probability": ml_prob,
            "explanation": explanation,
            "confidence_score": confidence,
            "agent_decision": agent_decision,
            "customer_response": customer_response,
            "final_outcome": final_outcome,
        })

    return pd.DataFrame(records)


# ──────────────────────────────────────────────────────────────────────
# CONVERSATIONS
# ──────────────────────────────────────────────────────────────────────
def generate_conversations(rng, risk_events_df, transactions_df):
    """
    Generate realistic AI agent conversations for medium/high/critical risk events.
    Each conversation has 2-6 turns.
    """
    records = []
    conv_counter = 0

    # Only generate conversations for medium+ risk events
    eligible = risk_events_df[risk_events_df["risk_level"].isin(["Medium", "High", "Critical"])]

    agent_greetings = [
        "I've reviewed your recent transaction and noticed some patterns I'd like to discuss with you. This is to ensure your financial safety.",
        "Before processing this transaction, I'd like to verify a few things with you. This is part of our decision intelligence system to protect you.",
        "I've detected some risk indicators in this transaction. Let me ask you a few questions to make sure everything is in order.",
    ]

    agent_followups = [
        "Thank you for sharing that. Could you also tell me {question}",
        "I appreciate your response. One more thing — {question}",
        "That's helpful. I also want to check — {question}",
        "Understood. For your safety, I need to ask — {question}",
    ]

    agent_safe_conclusions = [
        "Based on our conversation, I'm satisfied this is a legitimate transaction. You may proceed. Stay safe!",
        "Thank you for verifying. Everything checks out. Your transaction has been approved.",
        "I've confirmed the details. This appears to be a genuine transaction. Please proceed.",
    ]

    agent_warn_conclusions = [
        "Based on our conversation, I have significant concerns about this transaction. I strongly recommend you verify through official channels before proceeding.",
        "Several red flags have been identified. While I can't stop you, I urge extreme caution. Please consider cancelling this transaction.",
        "This transaction matches known scam patterns. I've flagged it for your protection. If you still wish to proceed, you do so at your own risk.",
    ]

    for _, event in eligible.iterrows():
        conv_counter += 1
        conv_id = f"CONV{conv_counter:06d}"
        txn_id = event["transaction_id"]
        cust_id = event["customer_id"]
        risk_level = event["risk_level"]

        # Number of turns based on risk level
        if risk_level == "Critical":
            n_turns = rng.integers(4, 7)
        elif risk_level == "High":
            n_turns = rng.integers(3, 6)
        else:
            n_turns = rng.integers(2, 4)

        base_time = datetime(2026, 1, 1) + timedelta(
            days=int(rng.integers(0, 180)),
            hours=int(rng.integers(8, 22)),
            minutes=int(rng.integers(0, 60))
        )

        seq = 0
        is_scam_scenario = risk_level in ("High", "Critical") and rng.random() < 0.6

        # Turn 1: Agent greeting
        seq += 1
        records.append({
            "conversation_id": conv_id,
            "customer_id": cust_id,
            "transaction_id": txn_id,
            "conversation_turn": seq,
            "speaker": "Agent",
            "message": rng.choice(agent_greetings),
            "intent": "greeting",
            "sentiment": "neutral",
            "agent_action": "initiate_conversation",
            "conversation_timestamp": (base_time + timedelta(seconds=seq * 15)).strftime("%Y-%m-%d %H:%M:%S"),
        })

        # Middle turns: Q&A
        available_questions = list(AGENT_QUESTIONS)
        rng.shuffle(available_questions)

        for turn in range(n_turns - 1):
            seq += 1
            if turn < len(available_questions):
                question = available_questions[turn]
            else:
                question = "Is there anything else you'd like to share about this transaction?"

            # Agent asks
            if turn == 0:
                agent_msg = question
            else:
                template = rng.choice(agent_followups)
                agent_msg = template.format(question=question.lower())

            records.append({
                "conversation_id": conv_id,
                "customer_id": cust_id,
                "transaction_id": txn_id,
                "conversation_turn": seq,
                "speaker": "Agent",
                "message": agent_msg,
                "intent": "verify_intent",
                "sentiment": "neutral",
                "agent_action": "ask_verification_question",
                "conversation_timestamp": (base_time + timedelta(seconds=seq * 20)).strftime("%Y-%m-%d %H:%M:%S"),
            })

            # Customer responds
            seq += 1
            if is_scam_scenario:
                response = rng.choice(SUSPICIOUS_RESPONSES)
                sentiment = rng.choice(["defensive", "anxious", "evasive"])
                intent = "suspicious_response"
            else:
                response_template = rng.choice(SAFE_RESPONSES)
                response = response_template.format(
                    relation=rng.choice(["brother", "sister", "friend", "colleague", "mother", "father"]),
                    years=rng.integers(2, 15),
                    category=rng.choice(["rent", "grocery", "utility", "insurance"])
                )
                sentiment = rng.choice(["confident", "calm", "cooperative"])
                intent = "safe_response"

            records.append({
                "conversation_id": conv_id,
                "customer_id": cust_id,
                "transaction_id": txn_id,
                "conversation_turn": seq,
                "speaker": "Customer",
                "message": response,
                "intent": intent,
                "sentiment": sentiment,
                "agent_action": "none",
                "conversation_timestamp": (base_time + timedelta(seconds=seq * 25)).strftime("%Y-%m-%d %H:%M:%S"),
            })

        # Final turn: Agent conclusion
        seq += 1
        if is_scam_scenario:
            conclusion = rng.choice(agent_warn_conclusions)
            agent_action = "warn_customer"
        else:
            conclusion = rng.choice(agent_safe_conclusions)
            agent_action = "approve_transaction"

        records.append({
            "conversation_id": conv_id,
            "customer_id": cust_id,
            "transaction_id": txn_id,
            "conversation_turn": seq,
            "speaker": "Agent",
            "message": conclusion,
            "intent": "conclusion",
            "sentiment": "assertive" if is_scam_scenario else "positive",
            "agent_action": agent_action,
            "conversation_timestamp": (base_time + timedelta(seconds=seq * 15)).strftime("%Y-%m-%d %H:%M:%S"),
        })

    return pd.DataFrame(records)


# ──────────────────────────────────────────────────────────────────────
# FEEDBACK
# ──────────────────────────────────────────────────────────────────────
def generate_feedback(rng, risk_events_df, conversations_df):
    """
    Generate customer feedback for ~60% of risk events.
    Feedback provides ground truth labels for model retraining.
    """
    records = []
    feedback_counter = 0

    # Get conversation IDs mapped to transaction IDs
    if len(conversations_df) > 0:
        conv_txn_map = conversations_df.groupby("transaction_id")["conversation_id"].first().to_dict()
    else:
        conv_txn_map = {}

    comments_helpful = [
        "The warning was accurate. Thank you for protecting me.",
        "Good catch! This was indeed a scam attempt.",
        "The AI conversation helped me understand the risk.",
        "I appreciate the system catching this suspicious transaction.",
        "Very helpful warning. I almost fell for a scam.",
    ]
    comments_false_alarm = [
        "This was a legitimate transaction. The warning was unnecessary.",
        "I know this person well. The alert was a false alarm.",
        "Regular payment flagged incorrectly.",
        "My usual monthly transfer was blocked. Please improve.",
    ]
    comments_neutral = [
        "The system works as expected.",
        "Acceptable experience overall.",
        "Transaction processed after verification.",
    ]

    for _, event in risk_events_df.iterrows():
        # ~60% of risk events get feedback
        if rng.random() > 0.60:
            continue

        feedback_counter += 1
        txn_id = event["transaction_id"]
        cust_id = event["customer_id"]
        conv_id = conv_txn_map.get(txn_id)
        final_outcome = event["final_outcome"]
        risk_level = event["risk_level"]

        # Customer action
        cust_resp = event["customer_response"]
        verified = cust_resp in ("Verified and Proceeded", "Proceeded")
        cancelled = cust_resp == "Cancelled"
        continued_anyway = cust_resp == "Proceeded Anyway"

        # Feedback type and rating
        if final_outcome == "Fraud Confirmed":
            feedback_type = "helpful"
            rating = rng.integers(4, 6)  # 4-5
            comment = rng.choice(comments_helpful)
            was_scam = True
        elif final_outcome == "Prevented" and risk_level in ("High", "Critical"):
            feedback_type = rng.choice(["helpful", "false_alarm"], p=[0.7, 0.3])
            rating = rng.integers(3, 6) if feedback_type == "helpful" else rng.integers(1, 4)
            comment = rng.choice(comments_helpful if feedback_type == "helpful" else comments_false_alarm)
            was_scam = feedback_type == "helpful"
        elif final_outcome == "False Alarm":
            feedback_type = "false_alarm"
            rating = rng.integers(1, 4)  # 1-3
            comment = rng.choice(comments_false_alarm)
            was_scam = False
        else:
            feedback_type = rng.choice(["helpful", "neutral"], p=[0.4, 0.6])
            rating = rng.integers(3, 5)
            comment = rng.choice(comments_neutral)
            was_scam = rng.random() < 0.1

        records.append({
            "feedback_id": f"FBK{feedback_counter:06d}",
            "customer_id": cust_id,
            "transaction_id": txn_id,
            "conversation_id": conv_id,
            "customer_action": cust_resp,
            "verified": verified,
            "cancelled": cancelled,
            "continued": continued_anyway,
            "feedback_rating": int(rating),
            "feedback_comment": comment,
            "timestamp": (datetime(2026, 1, 1) + timedelta(
                days=int(rng.integers(0, 180)),
                hours=int(rng.integers(8, 22))
            )).strftime("%Y-%m-%d %H:%M:%S"),
        })

    return pd.DataFrame(records)
