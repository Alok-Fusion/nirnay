import logging
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from ai.state.decision_state import DecisionState
from ai.schemas.interpretation import EvidenceReport
from ai.registry.llm_factory import llm_factory
from ai.prompts.templates import INTERPRETATION_SYSTEM_PROMPT
from ai.observability.metrics import trace_agent

logger = logging.getLogger(__name__)

@trace_agent("RiskInterpretationAgent")
def interpretation_agent(state: DecisionState) -> Dict[str, Any]:
    """
    Converts technical ML outputs into human-readable evidence.
    """
    context_data = state.get("context")
    if not context_data:
        raise ValueError("DecisionContext is missing in state.")
    from ai.schemas.context import DecisionContext
    context = DecisionContext(**context_data)

    # Initialize LLM with structured output mapping to EvidenceReport
    llm = llm_factory.get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(EvidenceReport)
    
    # Construct context string for the LLM
    tx = context.transaction
    risk = context.ml_risk
    recip = context.recipient
    
    human_msg = f"""
Transaction ID: {tx.transaction_id}
Amount: {tx.amount} {tx.currency}
Type: {tx.type}

Risk Score: {risk.risk_score} (Level: {risk.risk_level})
Confidence: {risk.confidence}
Reason Codes: {risk.reason_codes}
SHAP Values: {risk.shap_values}

Recipient Info:
New Recipient: {recip.is_new if recip else 'Unknown'}
Trusted: {recip.is_trusted if recip else 'Unknown'}
"""

    messages = [
        SystemMessage(content=INTERPRETATION_SYSTEM_PROMPT),
        HumanMessage(content=human_msg)
    ]
    
    evidence_report = structured_llm.invoke(messages)
    
    return {
        "evidence": evidence_report.model_dump(),
        "next_agent": "PolicyAgent",
        "workflow_status": "RUNNING"
    }
