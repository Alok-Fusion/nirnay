import logging
import json
from typing import Dict, Any
from ai.state.decision_state import DecisionState
from ai.observability.metrics import trace_agent

logger = logging.getLogger(__name__)

@trace_agent("AuditLogger")
def audit_logger(state: DecisionState) -> Dict[str, Any]:
    """
    Consolidates the entire decision logic, state changes, and actions into a final audit log.
    Outputs a structured trace.
    """
    print("\n" + "="*50)
    print("🔒 NIRNAY IMMUTABLE AUDIT LOG")
    print("="*50)
    
    tx_id = state.get("transaction_id", "UNKNOWN")
    case_id = state.get("case_id", "N/A")
    context = state.get("context", {})
    policy = state.get("policy_decision", {})
    decision = state.get("decision_result", {})
    conv = state.get("conversation_state", {})
    messages = state.get("messages", [])
    
    risk_score = context.get("ml_risk", {}).get("risk_score", 0.0)
    intent = conv.get("customer_intent", "UNKNOWN")
    
    # 1. Transaction Received
    print(f"[{tx_id}] Transaction Received.")
    
    # 2. Risk Evaluated
    print(f"[{tx_id}] Risk Score Calculated: {risk_score}")
    
    # 3. Policy Applied
    print(f"[{tx_id}] Policy Evaluated. Base Action: {policy.get('action')}")
    
    # 4. Customer Interaction
    if messages:
        print(f"[{tx_id}] Conversation Occurred. Attempts: {conv.get('confirmation_attempts', 0)}")
        print(f"[{tx_id}] Detected Customer Intent: {intent}")
    
    # 5. Decision & Execution
    d_result = decision.get('decision', 'UNKNOWN')
    print(f"[{tx_id}] Final Decision Generated: {d_result}")
    print(f"[{tx_id}] Reason: {decision.get('reason', '')}")
    
    if case_id and case_id != "N/A":
        print(f"[{tx_id}] ⚠️ Case Created: {case_id}")
        
    print("="*50 + "\n")
    
    return {
        "next_agent": "MemoryAgent" # Finally write to memory
    }
