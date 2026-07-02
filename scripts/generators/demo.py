"""
NIRNAY — Demo Scenario Generator
==================================
Generates: 12 complete demo scenario JSON files for hackathon judging.

Each scenario is a self-contained, realistic banking situation with
pre-built customer profiles, transactions, risk assessments, AI
explanations, conversation flows, and expected outcomes.
"""

import json
import os
import numpy as np


def generate_demo_scenarios(output_dir):
    """Generate all demo scenario JSON files to output_dir."""
    os.makedirs(output_dir, exist_ok=True)

    scenarios = [
        # ── 1. Normal Transfer ─────────────────────────────────
        {
            "scenario_id": "normal_transfer",
            "display_name": "Normal Transfer — Family Support",
            "description": "A routine monthly transfer to a family member. No risk indicators. Demonstrates the happy path.",
            "icon": "check_circle",
            "risk_category": "Safe",
            "customer": {
                "customer_id": "DEMO-CUS-001",
                "full_name": "Aarav Sharma",
                "age": 32,
                "occupation": "Software Engineer",
                "city": "Bangalore",
                "monthly_income": 120000,
                "average_transaction": 8000,
                "credit_score": 780,
                "risk_profile": "Conservative"
            },
            "transaction": {
                "amount": 15000,
                "currency": "INR",
                "category": "Transfer",
                "payment_channel": "UPI",
                "purpose": "Monthly family support to parents",
                "recipient": {
                    "name": "Rajesh Sharma",
                    "relationship": "Family",
                    "bank": "State Bank of India",
                    "trusted": True,
                    "transaction_count": 24,
                    "first_added": "2024-01-15"
                }
            },
            "expected_risk": {
                "risk_score": 8,
                "risk_level": "Low",
                "verdict": "Auto-Approve",
                "risk_factors": [
                    {"factor": "Trusted recipient", "impact": -5, "description": "24 prior transactions with this recipient"},
                    {"factor": "Family relationship", "impact": -3, "description": "Recipient is marked as family"},
                    {"factor": "Normal amount", "impact": 0, "description": "Within 2x of average transaction amount"}
                ]
            },
            "expected_explanation": "This is a routine transfer to a trusted family member. The amount is within your normal range, and you have 24 previous transactions with this recipient. No risk indicators detected.",
            "expected_conversation": None,
            "expected_decision": "auto_approved"
        },

        # ── 2. Salary Credit ──────────────────────────────────
        {
            "scenario_id": "salary_credit",
            "display_name": "Salary Credit — Monthly Payroll",
            "description": "Regular monthly salary deposit from employer. Zero risk. Demonstrates credit transaction handling.",
            "icon": "account_balance_wallet",
            "risk_category": "Safe",
            "customer": {
                "customer_id": "DEMO-CUS-002",
                "full_name": "Priya Patel",
                "age": 28,
                "occupation": "Data Scientist",
                "city": "Mumbai",
                "monthly_income": 150000,
                "average_transaction": 12000,
                "credit_score": 810,
                "risk_profile": "Moderate"
            },
            "transaction": {
                "amount": 150000,
                "currency": "INR",
                "category": "Salary",
                "payment_channel": "NEFT",
                "purpose": "Monthly salary - June 2026",
                "recipient": {
                    "name": "TechCorp Solutions Pvt Ltd",
                    "relationship": "Business",
                    "bank": "HDFC Bank",
                    "trusted": True,
                    "transaction_count": 18,
                    "first_added": "2025-01-01"
                }
            },
            "expected_risk": {
                "risk_score": 3,
                "risk_level": "Low",
                "verdict": "Auto-Approve",
                "risk_factors": []
            },
            "expected_explanation": "Regular salary credit from known employer. No risk indicators.",
            "expected_conversation": None,
            "expected_decision": "auto_approved"
        },

        # ── 3. Utility Payment ────────────────────────────────
        {
            "scenario_id": "utility_payment",
            "display_name": "Utility Payment — Electricity Bill",
            "description": "Monthly electricity bill payment to a verified utility provider.",
            "icon": "bolt",
            "risk_category": "Safe",
            "customer": {
                "customer_id": "DEMO-CUS-003",
                "full_name": "Vikram Reddy",
                "age": 45,
                "occupation": "Business Owner",
                "city": "Hyderabad",
                "monthly_income": 200000,
                "average_transaction": 15000,
                "credit_score": 750,
                "risk_profile": "Moderate"
            },
            "transaction": {
                "amount": 4500,
                "currency": "INR",
                "category": "Utilities",
                "payment_channel": "Auto Debit",
                "purpose": "Electricity bill - June 2026",
                "recipient": {
                    "name": "TSSPDCL",
                    "relationship": "Merchant",
                    "bank": "State Bank of India",
                    "trusted": True,
                    "transaction_count": 36,
                    "first_added": "2023-06-01"
                }
            },
            "expected_risk": {
                "risk_score": 5,
                "risk_level": "Low",
                "verdict": "Auto-Approve",
                "risk_factors": []
            },
            "expected_explanation": "Routine utility payment to a verified provider.",
            "expected_conversation": None,
            "expected_decision": "auto_approved"
        },

        # ── 4. Investment Scam ────────────────────────────────
        {
            "scenario_id": "investment_scam",
            "display_name": "Investment Scam — Guaranteed Returns",
            "description": "Transfer to a fraudulent investment scheme promising 40% monthly returns. Classic Ponzi scheme indicators.",
            "icon": "trending_up",
            "risk_category": "High Risk",
            "customer": {
                "customer_id": "DEMO-CUS-004",
                "full_name": "Ankit Gupta",
                "age": 38,
                "occupation": "Sales Executive",
                "city": "Delhi",
                "monthly_income": 55000,
                "average_transaction": 5000,
                "credit_score": 680,
                "risk_profile": "Moderate"
            },
            "transaction": {
                "amount": 50000,
                "currency": "INR",
                "category": "Investment",
                "payment_channel": "NEFT",
                "purpose": "Investment in Guaranteed Returns Scheme - promised 40% monthly returns by WhatsApp group admin",
                "recipient": {
                    "name": "GR Investments Pvt Ltd",
                    "relationship": "Unknown",
                    "bank": "Yes Bank",
                    "trusted": False,
                    "transaction_count": 0,
                    "first_added": "2026-06-28"
                }
            },
            "expected_risk": {
                "risk_score": 82,
                "risk_level": "High",
                "verdict": "Trigger Agentic Conversation",
                "risk_factors": [
                    {"factor": "Scam pattern match", "impact": 30, "description": "Purpose matches 'guaranteed returns' investment scam pattern (92% similarity)"},
                    {"factor": "New unknown recipient", "impact": 20, "description": "First-ever transfer to this entity, added 2 days ago"},
                    {"factor": "10x above average", "impact": 18, "description": "Amount is 10x your typical transaction of ₹5,000"},
                    {"factor": "Urgency language", "impact": 8, "description": "Contains urgency markers suggesting social pressure"},
                    {"factor": "Unknown relationship", "impact": 6, "description": "No established relationship with recipient"}
                ]
            },
            "expected_explanation": "This transaction exhibits multiple red flags consistent with investment scam patterns. No legitimate investment can guarantee 40% monthly returns. The recipient was added only 2 days ago, and the amount is 10x your average. This pattern matches known Ponzi schemes operating via WhatsApp groups.",
            "expected_conversation": [
                {"turn": 1, "speaker": "Agent", "message": "I've detected significant risk indicators in this transaction. Before processing, I need to verify a few things. How did you first learn about this investment opportunity?"},
                {"turn": 2, "speaker": "Customer", "message": "Someone in a WhatsApp group shared it. They showed screenshots of their profits."},
                {"turn": 3, "speaker": "Agent", "message": "Thank you. Screenshots of profits are easily fabricated and are a hallmark of Ponzi schemes. Have you independently verified if 'GR Investments Pvt Ltd' is registered with SEBI or any financial regulator?"},
                {"turn": 4, "speaker": "Customer", "message": "No, I haven't checked with SEBI. The admin said registration isn't needed for this type of scheme."},
                {"turn": 5, "speaker": "Agent", "message": "That's a major red flag. ALL legitimate investment schemes in India must be registered with SEBI. Guaranteeing 40% monthly returns is mathematically unsustainable and illegal under SEBI regulations. I strongly recommend cancelling this transaction. This matches patterns of known Ponzi schemes that have caused significant financial losses."},
                {"turn": 6, "speaker": "Customer", "message": "Thank you for the warning. I didn't realize this was a scam. I will cancel."}
            ],
            "expected_decision": "user_cancelled"
        },

        # ── 5. Crypto Scam ────────────────────────────────────
        {
            "scenario_id": "crypto_scam",
            "display_name": "Crypto Scam — Doubling Scheme",
            "description": "Cryptocurrency doubling scheme promoted via Telegram with AI trading claims.",
            "icon": "currency_bitcoin",
            "risk_category": "High Risk",
            "customer": {
                "customer_id": "DEMO-CUS-005",
                "full_name": "Rohan Mehta",
                "age": 25,
                "occupation": "Freelancer",
                "city": "Pune",
                "monthly_income": 45000,
                "average_transaction": 3000,
                "credit_score": 650,
                "risk_profile": "Aggressive"
            },
            "transaction": {
                "amount": 100000,
                "currency": "INR",
                "category": "Investment",
                "payment_channel": "IMPS",
                "purpose": "Deposit to CryptoAI Trading - guaranteed 2x returns in 24 hours using proprietary AI algorithm",
                "recipient": {
                    "name": "CryptoAI Global",
                    "relationship": "Unknown",
                    "bank": "IndusInd Bank",
                    "trusted": False,
                    "transaction_count": 0,
                    "first_added": "2026-06-30"
                }
            },
            "expected_risk": {
                "risk_score": 88,
                "risk_level": "High",
                "verdict": "Trigger Agentic Conversation",
                "risk_factors": [
                    {"factor": "Crypto scam pattern", "impact": 35, "description": "Matches known crypto doubling scheme (95% similarity)"},
                    {"factor": "Extreme amount deviation", "impact": 25, "description": "33x your average transaction"},
                    {"factor": "Brand new recipient", "impact": 15, "description": "Recipient added today"},
                    {"factor": "Unrealistic claims", "impact": 8, "description": "Guaranteed 2x returns in 24 hours is mathematically impossible"},
                    {"factor": "AI hype exploitation", "impact": 5, "description": "Uses AI buzzwords to create false credibility"}
                ]
            },
            "expected_explanation": "This transaction matches a known cryptocurrency doubling scam pattern. No legitimate trading platform can guarantee 2x returns in 24 hours. The use of 'AI algorithm' claims is a common tactic to create false credibility. The recipient was added today and the amount is 33x your average.",
            "expected_conversation": [
                {"turn": 1, "speaker": "Agent", "message": "This transaction has triggered our highest risk alerts. The platform 'CryptoAI Global' promises guaranteed 2x returns in 24 hours. Can you tell me how you discovered this platform?"},
                {"turn": 2, "speaker": "Customer", "message": "A friend on Telegram shared the link. He said he already doubled his money."},
                {"turn": 3, "speaker": "Agent", "message": "Telegram is the most common platform for crypto scam distribution. Your friend may either be part of the scheme or also a victim. Have you verified that CryptoAI Global is registered with any financial regulator?"},
                {"turn": 4, "speaker": "Customer", "message": "I didn't check. But they have a professional website with testimonials."},
                {"turn": 5, "speaker": "Agent", "message": "Professional websites are trivially easy to create. I strongly recommend cancelling this transaction. No legitimate investment can guarantee doubling your money in 24 hours. This follows the exact pattern of crypto Ponzi schemes that have collectively stolen billions globally."}
            ],
            "expected_decision": "user_cancelled"
        },

        # ── 6. Romance Scam ───────────────────────────────────
        {
            "scenario_id": "romance_scam",
            "display_name": "Romance Scam — Emergency Medical Funds",
            "description": "Online partner requesting emergency funds for a medical situation.",
            "icon": "favorite",
            "risk_category": "Medium Risk",
            "customer": {
                "customer_id": "DEMO-CUS-006",
                "full_name": "Sneha Nair",
                "age": 34,
                "occupation": "Teacher",
                "city": "Kochi",
                "monthly_income": 40000,
                "average_transaction": 4000,
                "credit_score": 720,
                "risk_profile": "Conservative"
            },
            "transaction": {
                "amount": 75000,
                "currency": "INR",
                "category": "Transfer",
                "payment_channel": "NEFT",
                "purpose": "Emergency medical help for partner - surgery needed urgently",
                "recipient": {
                    "name": "Michael Roberts",
                    "relationship": "Unknown",
                    "bank": "ICICI Bank",
                    "trusted": False,
                    "transaction_count": 2,
                    "first_added": "2026-05-15"
                }
            },
            "expected_risk": {
                "risk_score": 65,
                "risk_level": "High",
                "verdict": "Trigger Agentic Conversation",
                "risk_factors": [
                    {"factor": "Romance scam pattern", "impact": 22, "description": "Emergency medical fund request from recent online contact"},
                    {"factor": "High amount deviation", "impact": 18, "description": "Nearly 19x your average transaction"},
                    {"factor": "Recent untrusted recipient", "impact": 12, "description": "Only 2 prior transactions, added 6 weeks ago"},
                    {"factor": "Emotional urgency", "impact": 8, "description": "Contains emotional pressure and urgency language"},
                    {"factor": "Foreign-sounding name", "impact": 5, "description": "Name pattern commonly used in romance scams"}
                ]
            },
            "expected_explanation": "This transaction shows patterns consistent with romance scams. The combination of an online relationship, medical emergency urgency, and a large transfer to a recently-added contact are classic indicators.",
            "expected_conversation": [
                {"turn": 1, "speaker": "Agent", "message": "I want to ask you about this transfer. Can you tell me how you know Michael Roberts and how long you've been in contact?"},
                {"turn": 2, "speaker": "Customer", "message": "We met on a dating app about 2 months ago. He's been very caring and we talk every day."},
                {"turn": 3, "speaker": "Agent", "message": "Have you ever met Michael in person or had a video call with him?"},
                {"turn": 4, "speaker": "Customer", "message": "Not in person. He's based abroad. We've only done voice calls - he says his camera is broken."},
                {"turn": 5, "speaker": "Agent", "message": "I need to share something important. This follows a very common pattern of romance scams: an online relationship where the person avoids video calls, builds emotional connection, and then requests money for an emergency. 75,000 rupees is a significant amount. I strongly recommend not sending this until you can independently verify his identity and situation."},
                {"turn": 6, "speaker": "Customer", "message": "But what if he really is in trouble? I care about him."},
                {"turn": 7, "speaker": "Agent", "message": "Your compassion is understandable, but protecting yourself is important. If Michael is genuine, he will understand your need to verify. I suggest: 1) Request a video call before any transfer. 2) Ask for hospital details you can independently verify. 3) Never send money to someone you haven't met in person. Would you like to reconsider this transaction?"}
            ],
            "expected_decision": "user_cancelled"
        },

        # ── 7. Deepfake Scam ──────────────────────────────────
        {
            "scenario_id": "deepfake_scam",
            "display_name": "Deepfake Scam — Boss Impersonation",
            "description": "AI-generated voice clone impersonating the customer's boss, requesting an urgent vendor payment.",
            "icon": "face_retouching_off",
            "risk_category": "High Risk",
            "customer": {
                "customer_id": "DEMO-CUS-007",
                "full_name": "Kavya Joshi",
                "age": 29,
                "occupation": "Business Analyst",
                "city": "Gurgaon",
                "monthly_income": 80000,
                "average_transaction": 6000,
                "credit_score": 740,
                "risk_profile": "Conservative"
            },
            "transaction": {
                "amount": 200000,
                "currency": "INR",
                "category": "Transfer",
                "payment_channel": "NEFT",
                "purpose": "Urgent vendor payment as instructed by director - confidential",
                "recipient": {
                    "name": "FastTrack Solutions",
                    "relationship": "Unknown",
                    "bank": "Axis Bank",
                    "trusted": False,
                    "transaction_count": 0,
                    "first_added": "2026-06-30"
                }
            },
            "expected_risk": {
                "risk_score": 78,
                "risk_level": "High",
                "verdict": "Trigger Agentic Conversation",
                "risk_factors": [
                    {"factor": "Deepfake pattern match", "impact": 25, "description": "Voice-instructed urgent payment to unknown vendor matches deepfake scam pattern"},
                    {"factor": "Extreme amount", "impact": 22, "description": "33x your average transaction"},
                    {"factor": "New recipient", "impact": 15, "description": "Brand new recipient added today"},
                    {"factor": "Confidentiality request", "impact": 10, "description": "'Confidential' keyword is a manipulation tactic"},
                    {"factor": "Authority pressure", "impact": 6, "description": "Instruction from authority figure creates compliance pressure"}
                ]
            },
            "expected_explanation": "This transaction exhibits hallmarks of deepfake voice-clone fraud. Scammers use AI to clone a boss's voice and instruct urgent, confidential payments to unknown vendors.",
            "expected_conversation": [
                {"turn": 1, "speaker": "Agent", "message": "This transaction raises serious concerns. You mentioned this was instructed by your director. Did you receive this instruction via a phone call?"},
                {"turn": 2, "speaker": "Customer", "message": "Yes, my director called me and asked me to make this payment urgently to a new vendor."},
                {"turn": 3, "speaker": "Agent", "message": "Were you asked to keep this payment confidential or not discuss it with other colleagues?"},
                {"turn": 4, "speaker": "Customer", "message": "Yes, he said it's a sensitive deal and I shouldn't discuss it with anyone."},
                {"turn": 5, "speaker": "Agent", "message": "This is a critical red flag. AI voice-cloning technology can now replicate anyone's voice from just a few minutes of audio. The combination of urgency, confidentiality, and a new unknown recipient is the exact pattern of deepfake CEO fraud. I strongly recommend you: 1) Call your director back on their known number. 2) Verify the payment through your company's standard approval process. 3) Do NOT proceed based solely on a phone call."}
            ],
            "expected_decision": "user_cancelled"
        },

        # ── 8. Fake Bank Officer ──────────────────────────────
        {
            "scenario_id": "fake_bank_officer",
            "display_name": "Fake Bank Officer — KYC Update Fraud",
            "description": "Caller impersonating bank officer threatening account freeze unless KYC fee is paid immediately.",
            "icon": "security",
            "risk_category": "Critical Risk",
            "customer": {
                "customer_id": "DEMO-CUS-008",
                "full_name": "Sunita Verma",
                "age": 58,
                "occupation": "Retired",
                "city": "Jaipur",
                "monthly_income": 35000,
                "average_transaction": 3000,
                "credit_score": 700,
                "risk_profile": "Conservative"
            },
            "transaction": {
                "amount": 25000,
                "currency": "INR",
                "category": "Transfer",
                "payment_channel": "IMPS",
                "purpose": "KYC update fee - bank officer Mr Kapoor said account will be frozen in 2 hours if not paid",
                "recipient": {
                    "name": "Rajiv Kapoor",
                    "relationship": "Unknown",
                    "bank": "HDFC Bank",
                    "trusted": False,
                    "transaction_count": 0,
                    "first_added": "2026-06-30"
                }
            },
            "expected_risk": {
                "risk_score": 94,
                "risk_level": "Critical",
                "verdict": "Auto-Block",
                "risk_factors": [
                    {"factor": "Bank impersonation pattern", "impact": 35, "description": "Exact match with 'KYC Update Fraud' scam pattern"},
                    {"factor": "Account freeze threat", "impact": 20, "description": "Threat-based urgency is a hallmark of impersonation scams"},
                    {"factor": "Payment to personal account", "impact": 18, "description": "Banks never collect fees via personal accounts"},
                    {"factor": "New unknown recipient", "impact": 12, "description": "Brand new personal recipient"},
                    {"factor": "Vulnerable profile", "impact": 9, "description": "Retired customers are disproportionately targeted"}
                ]
            },
            "expected_explanation": "BLOCKED: This transaction has been automatically blocked. Banks NEVER charge KYC fees through personal transfers. No bank officer will ask you to transfer money to a personal account. This is a known impersonation scam. Please contact your bank directly through the number on your card or bank statement.",
            "expected_conversation": None,
            "expected_decision": "system_blocked"
        },

        # ── 9. Lottery Scam ───────────────────────────────────
        {
            "scenario_id": "lottery_scam",
            "display_name": "Lottery Scam — WhatsApp Prize Winner",
            "description": "WhatsApp message claiming customer won ₹10 lakh lottery and needs to pay processing fee.",
            "icon": "emoji_events",
            "risk_category": "Critical Risk",
            "customer": {
                "customer_id": "DEMO-CUS-009",
                "full_name": "Deepak Singh",
                "age": 52,
                "occupation": "Shop Owner",
                "city": "Lucknow",
                "monthly_income": 30000,
                "average_transaction": 2500,
                "credit_score": 660,
                "risk_profile": "Moderate"
            },
            "transaction": {
                "amount": 15000,
                "currency": "INR",
                "category": "Transfer",
                "payment_channel": "UPI",
                "purpose": "Processing fee for KBC lottery prize of Rs 10,00,000 - reference number KBC2026-98765",
                "recipient": {
                    "name": "KBC Prize Department",
                    "relationship": "Unknown",
                    "bank": "Punjab National Bank",
                    "trusted": False,
                    "transaction_count": 0,
                    "first_added": "2026-06-30"
                }
            },
            "expected_risk": {
                "risk_score": 96,
                "risk_level": "Critical",
                "verdict": "Auto-Block",
                "risk_factors": [
                    {"factor": "Lottery scam exact match", "impact": 40, "description": "KBC lottery prize fraud - one of India's most common scams"},
                    {"factor": "Advance fee demand", "impact": 25, "description": "Legitimate prizes never require upfront payment"},
                    {"factor": "New unknown entity", "impact": 15, "description": "No prior relationship with 'KBC Prize Department'"},
                    {"factor": "Impersonation", "impact": 10, "description": "KBC is a registered trademark - this entity is not affiliated"},
                    {"factor": "Unsolicited contact", "impact": 6, "description": "You cannot win a lottery you did not enter"}
                ]
            },
            "expected_explanation": "BLOCKED: This is a textbook lottery scam. KBC (Kaun Banega Crorepati) does NOT conduct lotteries or distribute prizes via WhatsApp. Legitimate prizes never require processing fees. This is one of the most common scams in India.",
            "expected_conversation": None,
            "expected_decision": "system_blocked"
        },

        # ── 10. Emergency Relative Scam ───────────────────────
        {
            "scenario_id": "emergency_relative",
            "display_name": "Emergency Relative — Fake Accident Claim",
            "description": "Caller claims customer's son was in an accident and needs immediate hospital payment.",
            "icon": "local_hospital",
            "risk_category": "High Risk",
            "customer": {
                "customer_id": "DEMO-CUS-010",
                "full_name": "Meera Iyer",
                "age": 55,
                "occupation": "Government Officer",
                "city": "Chennai",
                "monthly_income": 65000,
                "average_transaction": 5000,
                "credit_score": 730,
                "risk_profile": "Conservative"
            },
            "transaction": {
                "amount": 150000,
                "currency": "INR",
                "category": "Transfer",
                "payment_channel": "IMPS",
                "purpose": "Emergency hospital payment for son's accident - doctor said surgery needed immediately",
                "recipient": {
                    "name": "Dr. Venkat",
                    "relationship": "Unknown",
                    "bank": "Canara Bank",
                    "trusted": False,
                    "transaction_count": 0,
                    "first_added": "2026-06-30"
                }
            },
            "expected_risk": {
                "risk_score": 73,
                "risk_level": "High",
                "verdict": "Trigger Agentic Conversation",
                "risk_factors": [
                    {"factor": "Emergency scam pattern", "impact": 25, "description": "Fake medical emergency involving family member"},
                    {"factor": "Extreme urgency", "impact": 18, "description": "Pressure for immediate payment"},
                    {"factor": "Large amount to unknown", "impact": 15, "description": "₹1,50,000 to brand new recipient"},
                    {"factor": "Personal account", "impact": 10, "description": "Hospital payments go to hospital accounts, not personal accounts"},
                    {"factor": "Amount deviation", "impact": 5, "description": "30x your average transaction"}
                ]
            },
            "expected_explanation": "This transaction shows indicators of an emergency relative scam. Scammers create panic by claiming a family member is in danger and demand immediate payment to personal accounts instead of hospital accounts.",
            "expected_conversation": [
                {"turn": 1, "speaker": "Agent", "message": "I understand this feels urgent, but I need to verify a few things for your safety. Have you directly contacted your son to confirm the accident?"},
                {"turn": 2, "speaker": "Customer", "message": "The doctor said he's in surgery and can't talk. They told me to transfer immediately."},
                {"turn": 3, "speaker": "Agent", "message": "I need to point out something important: legitimate hospital payments go to the hospital's institutional account, not a personal account named 'Dr. Venkat'. Can you call your son's phone directly right now?"},
                {"turn": 4, "speaker": "Customer", "message": "Let me try... He picked up! He says he's fine and at work!"},
                {"turn": 5, "speaker": "Agent", "message": "I'm glad your son is safe. This was a scam. The caller exploited your parental concern to create panic. Please block the number that called you and report it to the cyber crime helpline (1930). Your transaction has been cancelled."}
            ],
            "expected_decision": "user_cancelled"
        },

        # ── 11. Business Payment ──────────────────────────────
        {
            "scenario_id": "business_payment",
            "display_name": "Business Payment — Vendor Invoice",
            "description": "Legitimate business payment to a regular vendor. Medium risk due to large amount.",
            "icon": "business",
            "risk_category": "Low Risk",
            "customer": {
                "customer_id": "DEMO-CUS-011",
                "full_name": "Rajesh Kapoor",
                "age": 48,
                "occupation": "Business Owner",
                "city": "Mumbai",
                "monthly_income": 300000,
                "average_transaction": 45000,
                "credit_score": 800,
                "risk_profile": "Moderate"
            },
            "transaction": {
                "amount": 250000,
                "currency": "INR",
                "category": "Transfer",
                "payment_channel": "RTGS",
                "purpose": "Invoice payment - INV-2026-0892 to regular supplier",
                "recipient": {
                    "name": "Sharma Textiles Pvt Ltd",
                    "relationship": "Business",
                    "bank": "HDFC Bank",
                    "trusted": True,
                    "transaction_count": 15,
                    "first_added": "2024-03-10"
                }
            },
            "expected_risk": {
                "risk_score": 22,
                "risk_level": "Low",
                "verdict": "Auto-Approve",
                "risk_factors": [
                    {"factor": "Large amount", "impact": 12, "description": "5.5x average but within business norms"},
                    {"factor": "Trusted vendor", "impact": -8, "description": "15 prior transactions over 2 years"},
                    {"factor": "Business relationship", "impact": -5, "description": "Established business relationship"}
                ]
            },
            "expected_explanation": "Large but legitimate business payment to a trusted vendor with established history.",
            "expected_conversation": None,
            "expected_decision": "auto_approved"
        },

        # ── 12. Large First-Time Transfer ─────────────────────
        {
            "scenario_id": "large_first_time",
            "display_name": "Large First-Time Transfer — Property Advance",
            "description": "Large transfer to a new recipient for property booking. Moderate risk requiring verification.",
            "icon": "home",
            "risk_category": "Medium Risk",
            "customer": {
                "customer_id": "DEMO-CUS-012",
                "full_name": "Siddharth Banerjee",
                "age": 35,
                "occupation": "Software Engineer",
                "city": "Bangalore",
                "monthly_income": 180000,
                "average_transaction": 15000,
                "credit_score": 790,
                "risk_profile": "Moderate"
            },
            "transaction": {
                "amount": 500000,
                "currency": "INR",
                "category": "Transfer",
                "payment_channel": "RTGS",
                "purpose": "Booking advance for flat in Whitefield - builder ABC Realty",
                "recipient": {
                    "name": "ABC Realty Developers",
                    "relationship": "Business",
                    "bank": "ICICI Bank",
                    "trusted": False,
                    "transaction_count": 0,
                    "first_added": "2026-06-29"
                }
            },
            "expected_risk": {
                "risk_score": 48,
                "risk_level": "Medium",
                "verdict": "Show Warning",
                "risk_factors": [
                    {"factor": "Very large amount", "impact": 20, "description": "33x your average transaction"},
                    {"factor": "New recipient", "impact": 15, "description": "First transaction with this entity"},
                    {"factor": "Real estate category", "impact": 8, "description": "Large real estate transactions warrant verification"},
                    {"factor": "Business entity", "impact": -5, "description": "Payment to a registered business name"}
                ]
            },
            "expected_explanation": "Large first-time transfer for property booking. While this could be legitimate, the amount is significant and the recipient is new. We recommend verifying the builder's RERA registration before proceeding.",
            "expected_conversation": [
                {"turn": 1, "speaker": "Agent", "message": "This is a large transfer to a new recipient. Can you confirm - have you visited the property and met the builder in person?"},
                {"turn": 2, "speaker": "Customer", "message": "Yes, I visited the site last week and have all the documentation. The builder is RERA registered."},
                {"turn": 3, "speaker": "Agent", "message": "Good. Since you've verified the builder's RERA registration and visited the property, this appears legitimate. I recommend keeping all documentation. You may proceed with caution."}
            ],
            "expected_decision": "user_approved"
        },
    ]

    # Write each scenario as a separate JSON file
    for scenario in scenarios:
        filename = f"{scenario['scenario_id']}.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(scenario, f, indent=2, ensure_ascii=False)

    # Also write a master index file
    index = {
        "total_scenarios": len(scenarios),
        "scenarios": [
            {
                "scenario_id": s["scenario_id"],
                "display_name": s["display_name"],
                "risk_category": s["risk_category"],
                "icon": s["icon"],
            }
            for s in scenarios
        ]
    }
    with open(os.path.join(output_dir, "_index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    return scenarios
