import logging
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from ai.state.decision_state import DecisionState
from ai.schemas.conversation import ConversationAction, ConversationState, CustomerIntent
from ai.registry.llm_factory import llm_factory
from ai.prompts.templates import CONVERSATION_SYSTEM_PROMPT
from ai.observability.metrics import trace_agent

logger = logging.getLogger(__name__)

@trace_agent("ConversationOrchestrator")
def conversation_agent(state: DecisionState) -> Dict[str, Any]:
    """
    Determines whether to Explain, Ask Questions, Recommend, Escalate, or End.
    """
    evidence_data = state.get("evidence")
    policy_data = state.get("policy_decision")
    messages = state.get("messages", [])
    
    if not evidence_data or not policy_data:
        raise ValueError("Missing evidence or policy for ConversationOrchestrator.")

    from ai.schemas.interpretation import EvidenceReport
    from ai.schemas.policy import PolicyDecision
    
    evidence = EvidenceReport(**evidence_data)
    policy_decision = PolicyDecision(**policy_data)

    llm = llm_factory.get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(ConversationAction)
    
    # Format conversation history
    history_str = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in messages])
    
    context_data = state.get("context")
    from ai.schemas.context import DecisionContext
    context = DecisionContext(**context_data) if context_data else None
    
    past_memories = context.historical_context.get("past_memories", []) if context and context.historical_context else []
    past_memories_str = "\n".join(past_memories) if past_memories else "No past transactions recorded."

    human_msg = f"""
Transaction Details:
Amount: {context.transaction.currency} {context.transaction.amount}
Recipient: {context.recipient.name if context.recipient else 'Unknown'}
Risk Score: {context.ml_risk.risk_score}

Policy Action: {policy_decision.action}
Requires Human Approval: {policy_decision.requires_human_approval}
Rationale: {policy_decision.rationale}
Recommendations: {", ".join(policy_decision.recommendations)}

Evidence Summary: {evidence.overall_summary}

Past Customer Memory Context:
{past_memories_str}

Conversation History:
{history_str}

Decide the next action to take with the user.
"""

    llm_messages = [
        SystemMessage(content=CONVERSATION_SYSTEM_PROMPT),
        HumanMessage(content=human_msg)
    ]
    
    # Output Validation & Retry Loop
    action = None
    max_retries = 1
    for attempt in range(max_retries + 1):
        try:
            action = structured_llm.invoke(llm_messages)
            break # Success
        except Exception as e:
            logger.warning(f"Structured output validation failed on attempt {attempt + 1}: {e}")
            if attempt < max_retries:
                # Add correction prompt
                error_msg = f"Your previous response failed schema validation with error: {e}\nEnsure booleans are native (e.g. `false` not `\"false\"`) and integers are native (e.g. `0` not `\"0\"`). Please retry and output valid JSON."
                llm_messages.append(HumanMessage(content=error_msg))
            else:
                # Fallback to prevent crash
                logger.error("Failed to generate valid structured output after retries.")
                action = ConversationAction(
                    action_type="AskQuestion",
                    message_to_customer="I'm sorry, I encountered an internal error processing that. Could you clarify your intent?",
                    requires_response=True,
                    updated_state=ConversationState(customer_intent=CustomerIntent.UNKNOWN)
                )
    
    # Check if workflow should pause for customer input
    workflow_status = "RUNNING"
    if action.requires_response:
        workflow_status = "AWAITING_CUSTOMER"
        next_agent = "HumanApproval" # Actually the orchestrator routing handles this based on status
        # but to be safe, we just set AWAITING_CUSTOMER and let route_next do the rest.
        
    return {
        "last_action": action.model_dump(),
        "conversation_state": action.updated_state.model_dump(),
        "next_agent": "DecisionResolutionEngine" if workflow_status == "RUNNING" else "HumanApproval",
        "workflow_status": workflow_status
    }
