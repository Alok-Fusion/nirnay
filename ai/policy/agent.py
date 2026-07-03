import logging
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from ai.state.decision_state import DecisionState
from ai.schemas.policy import PolicyDecision
from ai.registry.llm_factory import llm_factory
from ai.prompts.templates import POLICY_SYSTEM_PROMPT
from ai.observability.metrics import trace_agent

logger = logging.getLogger(__name__)

@trace_agent("PolicyAndComplianceAgent")
def policy_agent(state: DecisionState) -> Dict[str, Any]:
    """
    Evaluates context and evidence against business rules.
    """
    context_data = state.get("context")
    evidence_data = state.get("evidence")
    
    if not context_data or not evidence_data:
        raise ValueError("Missing context or evidence for PolicyAgent.")

    from ai.schemas.context import DecisionContext
    from ai.schemas.interpretation import EvidenceReport
    
    context = DecisionContext(**context_data)
    evidence = EvidenceReport(**evidence_data)

    llm = llm_factory.get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(PolicyDecision)
    
    human_msg = f"""
Context Summary:
Amount: {context.transaction.amount}
Risk Score: {context.ml_risk.risk_score}
Avg Transaction Amount: {context.behavior.avg_transaction_amount}
New Recipient: {context.recipient.is_new if context.recipient else True}

Evidence Summary:
{evidence.overall_summary}
Scam Typology: {evidence.scam_typology}
"""

    messages = [
        SystemMessage(content=POLICY_SYSTEM_PROMPT),
        HumanMessage(content=human_msg)
    ]
    
    policy_decision = structured_llm.invoke(messages)
    
    # If the policy requires human approval, we might want to ask the Conversation Orchestrator
    # to handle the questioning, or just transition to AWAITING_CUSTOMER directly in the graph.
    # The Prompt states Conversation Orchestrator determines whether to Explain/Ask/End.
    
    return {
        "policy_decision": policy_decision.model_dump(),
        "next_agent": "ConversationOrchestrator",
        "workflow_status": "RUNNING"
    }
