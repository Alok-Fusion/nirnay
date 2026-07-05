from typing import Dict, Any, Tuple, List

# Scam type labels returned alongside severity
SCAM_TYPE_INVESTMENT = "potential_investment_scam"
SCAM_TYPE_CRYPTO = "crypto_scam"
SCAM_TYPE_ROMANCE = "potential_romance_scam"
SCAM_TYPE_BEC = "potential_business_email_compromise"
SCAM_TYPE_VELOCITY = "velocity_fraud_attack"
SCAM_TYPE_SOCIAL_ENGINEERING = "social_engineering_pressure"
SCAM_TYPE_NONE = None

# Keywords that suggest investment/romance/BEC scams in recipient context
CRYPTO_KEYWORDS = ["crypto", "bitcoin", "btc", "ethereum", "eth", "usdt", "wallet", "binance", "coinbase", "okx", "bybit"]
INVESTMENT_KEYWORDS = ["invest", "return", "profit", "trading", "forex", "scheme", "opportunity", "stock", "fund"]
ROMANCE_KEYWORDS = ["love", "darling", "sweetheart", "gift", "emergency", "visa", "travel"]


class RuleEngine:
    @staticmethod
    def evaluate(features: Dict[str, Any], current_amount: float) -> Tuple[str, str, str]:
        """
        Evaluates the transaction against NIRNAY's Decision Intelligence policies.
        Returns a tuple: (RuleResult, HumanReason, ScamType)
        
        RuleResult: 'SAFE' | 'SUSPICIOUS' | 'HARD_BLOCK'
        HumanReason: Plain-language explanation for the customer and AI agents
        ScamType: Scam classification label or None
        """

        balance_after = features.get("balance_after", 0.0)
        is_trusted = bool(features.get("trusted_recipient", 0.0))
        recipient_tx_count = features.get("recipient_transfer_count", 0)
        is_night = bool(features.get("night_transaction", 0.0))
        tx_last_hour = features.get("transactions_last_hour", 0)
        tx_last_24h = features.get("transactions_last_24h", 0)
        amount_ratio = features.get("amount_ratio", 1.0)
        recipient_name = str(features.get("recipient_name", "")).lower()
        recipient_bank_code = str(features.get("recipient_bank_code", "")).lower()
        is_overseas = bool(features.get("is_overseas", 0))
        avg_amount = features.get("avg_transfer_amount", current_amount)

        triggered_factors: List[str] = []

        # ─────────────────────────────────────────────────────────
        # TIER 1: HARD BLOCKS — Non-negotiable. No AI involvement.
        # ─────────────────────────────────────────────────────────

        if balance_after < 0:
            return (
                "HARD_BLOCK",
                "This transfer cannot be completed — your account balance is insufficient.",
                SCAM_TYPE_NONE
            )

        # Crypto scam detection — any transfer to a crypto entity is blocked
        if any(kw in recipient_name for kw in CRYPTO_KEYWORDS) or \
           any(kw in recipient_bank_code for kw in CRYPTO_KEYWORDS):
            return (
                "HARD_BLOCK",
                (
                    "NIRNAY has detected this transfer is directed to a cryptocurrency platform. "
                    "RBI guidelines prohibit direct bank transfers to crypto exchanges due to the high risk "
                    "of irreversible fraud. This transaction has been blocked to protect your funds."
                ),
                SCAM_TYPE_CRYPTO
            )

        # Extreme velocity — account takeover or automated fraud attack
        if tx_last_hour > 5:
            return (
                "HARD_BLOCK",
                (
                    f"Your account has recorded {tx_last_hour} transfers in the last hour, "
                    "which exceeds the maximum allowed velocity. This pattern is associated with "
                    "account takeover attacks. The transfer has been blocked and your account is protected."
                ),
                SCAM_TYPE_VELOCITY
            )

        # New recipient + very large amount to overseas — BEC or romance scam
        if recipient_tx_count == 0 and is_overseas and current_amount > 50000:
            return (
                "HARD_BLOCK",
                (
                    "This is your first-ever transfer to this overseas recipient, and the amount is "
                    f"significantly large (₹{current_amount:,.0f}). Transfers of this nature to new "
                    "international contacts are a primary indicator of Business Email Compromise or "
                    "romance scams. This transfer has been blocked for your protection."
                ),
                SCAM_TYPE_BEC
            )

        # ─────────────────────────────────────────────────────────
        # TIER 2: SUSPICIOUS — Requires AI analysis & conversation
        # ─────────────────────────────────────────────────────────

        scam_type = SCAM_TYPE_NONE

        # Check transaction daily limit exceeded
        if features.get("limit_exceeded", 0.0) == 1.0:
            limit = features.get("daily_limit", 1000.0)
            spent = features.get("daily_spent_sum", 0.0)
            reason = f"Your daily transfer limit of ${limit:,.0f} has been reached (Spent today: ${spent:,.2f}). Proceeding requires security review."
            return ("SUSPICIOUS", reason, SCAM_TYPE_NONE)

        # Investment scam indicators
        if any(kw in recipient_name for kw in INVESTMENT_KEYWORDS):
            triggered_factors.append("Recipient name matches known investment scam patterns")
            scam_type = SCAM_TYPE_INVESTMENT

        # Romance scam indicators
        if any(kw in recipient_name for kw in ROMANCE_KEYWORDS) and recipient_tx_count == 0:
            triggered_factors.append("New recipient with profile matching romance or gift scam patterns")
            scam_type = SCAM_TYPE_ROMANCE

        # Social engineering pressure: large, urgent, unusual-hours transfer
        if is_night and current_amount > 2000 and recipient_tx_count == 0:
            triggered_factors.append(
                "Large transfer to a new recipient during unusual hours — a common pattern in social engineering"
            )
            scam_type = scam_type or SCAM_TYPE_SOCIAL_ENGINEERING

        # Significantly above average
        if amount_ratio > 4.0:
            triggered_factors.append(
                f"Transfer amount is {amount_ratio:.1f}× your historical average — significantly outside your normal behaviour"
            )

        # Large amount to new recipient
        if current_amount > 10000 and recipient_tx_count == 0 and not is_trusted:
            triggered_factors.append("Large transfer to a recipient you have never transacted with before")

        # High 24h volume
        if tx_last_24h >= 5:
            triggered_factors.append(
                f"You have already made {tx_last_24h} transfers today — unusual daily velocity"
            )
            scam_type = scam_type or SCAM_TYPE_VELOCITY

        # Overseas first-time
        if is_overseas and recipient_tx_count == 0:
            triggered_factors.append("First-ever transfer to an overseas account")
            scam_type = scam_type or SCAM_TYPE_ROMANCE

        if triggered_factors:
            reason = "NIRNAY has flagged this transfer for review. Factors identified: " + \
                     "; ".join(triggered_factors) + "."
            return ("SUSPICIOUS", reason, scam_type)

        # ─────────────────────────────────────────────────────────
        # TIER 3: SAFE — Bypass AI, go directly to authentication
        # ─────────────────────────────────────────────────────────

        if is_trusted and current_amount < 5000:
            return (
                "SAFE",
                "Transfer to a trusted recipient within your normal spending range. NIRNAY has verified this is consistent with your banking behaviour.",
                SCAM_TYPE_NONE
            )

        if current_amount < 500 and recipient_tx_count > 2:
            return (
                "SAFE",
                "Routine low-value transfer to a familiar recipient. No risk indicators detected.",
                SCAM_TYPE_NONE
            )

        if not is_night and amount_ratio < 1.5 and recipient_tx_count > 0:
            return (
                "SAFE",
                "Transfer is within your normal range and this recipient has received money from you before.",
                SCAM_TYPE_NONE
            )

        # Fallback: anything unclassified goes for contextual AI review
        return (
            "SUSPICIOUS",
            "NIRNAY is conducting a contextual review of this transfer before proceeding.",
            SCAM_TYPE_NONE
        )
