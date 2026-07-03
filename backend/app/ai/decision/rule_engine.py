from typing import Dict, Any, Tuple

class RuleEngine:
    @staticmethod
    def evaluate(features: Dict[str, Any], current_amount: float) -> Tuple[str, str]:
        """
        Evaluates the generated features against strict enterprise banking policies.
        Returns a tuple: (RuleResult, Reason)
        RuleResult can be: 'SAFE', 'SUSPICIOUS', 'HIGH_RISK'
        """
        
        amount = current_amount
        balance_after = features.get("balance_after", 0.0)
        is_trusted = bool(features.get("trusted_recipient", 0.0))
        recipient_tx_count = features.get("recipient_transfer_count", 0)
        is_night = bool(features.get("night_transaction", 0.0))
        tx_last_hour = features.get("transactions_last_hour", 0)
        amount_ratio = features.get("amount_ratio", 1.0)
        
        triggered_rules = []
        
        # --- HIGH RISK RULES (Deterministic Blocks) ---
        if balance_after < 0:
            return "HIGH_RISK", "Insufficient funds"
            
        if amount > 50000.0 and not is_trusted:
            return "HIGH_RISK", "Amount exceeds maximum threshold for untrusted recipient"
            
        if tx_last_hour > 5:
            return "HIGH_RISK", "Velocity limits exceeded (Too many transactions in 1 hour)"
            
        # --- SUSPICIOUS RULES (Requires AI/LangGraph) ---
        if amount > 10000.0:
            triggered_rules.append("Large amount")
            
        if recipient_tx_count == 0 and not is_trusted:
            triggered_rules.append("New untrusted recipient")
            
        if is_night and amount > 2000.0:
            triggered_rules.append("Large transaction during unusual hours")
            
        if amount_ratio > 3.0:
            triggered_rules.append("Amount significantly exceeds historical average")
            
        if len(triggered_rules) > 0:
            return "SUSPICIOUS", f"Triggered rules: {', '.join(triggered_rules)}"
            
        # --- SAFE RULES (Bypass AI) ---
        if is_trusted and amount < 5000.0:
            return "SAFE", "Standard transaction to trusted recipient"
            
        if amount < 500.0 and recipient_tx_count > 0:
            return "SAFE", "Low risk recurring transaction"
            
        # Fallback to suspicious for anything not explicitly safe
        return "SUSPICIOUS", "Transaction requires contextual baseline verification"
