import logging
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from ai.state.decision_state import DecisionState
from ai.context.agent import context_agent
from ai.interpretation.agent import interpretation_agent
from ai.policy.agent import policy_agent
from ai.conversation.agent import conversation_agent
from ai.decision.engine import decision_engine
from ai.action.executor import action_executor
from ai.audit.logger import audit_logger
from ai.memory.agent import memory_agent

import traceback

logger = logging.getLogger(__name__)

def safe_agent_wrapper(agent_func):
    """Wraps an agent function in a try-except block to gracefully handle failures."""
    def wrapper(state: DecisionState):
        try:
            return agent_func(state)
        except Exception as e:
            logger.error(f"Agent {agent_func.__name__} failed: {str(e)}\n{traceback.format_exc()}")
            return {
                "errors": [f"{agent_func.__name__} failed: {str(e)}"],
                "workflow_status": "FAILED",
                "next_agent": "END"
            }
    return wrapper

def route_next(state: DecisionState):
    """Router function to determine next node based on workflow_status."""
    status = state.get("workflow_status", "RUNNING")
    if status == "COMPLETED":
        if state.get("next_agent") == "END":
            return END
        # Normally ActionExecutor outputs COMPLETED and points to AuditLogger. AuditLogger -> MemoryAgent -> END
        return state.get("next_agent", "END")
    elif status == "AWAITING_CUSTOMER":
        return "HumanApproval"
    elif status == "FAILED":
        return END
    
    # If running, follow next_agent
    next_node = state.get("next_agent")
    if next_node == "END":
        return END
    return next_node

def human_approval_node(state: DecisionState):
    """
    A dummy node where the graph pauses.
    When resumed, it takes the user input from state.messages and proceeds.
    """
    logger.info("Resuming from Human Approval...")
    # In reality, this node just transitions to ConversationOrchestrator to evaluate the human's response
    # We must increment confirmation attempts
    conv = state.get("conversation_state", {})
    attempts = conv.get("confirmation_attempts", 0)
    conv["confirmation_attempts"] = attempts + 1
    
    return {"conversation_state": conv, "next_agent": "ConversationOrchestrator", "workflow_status": "RUNNING"}

def create_decision_graph():
    """Builds and compiles the LangGraph."""
    workflow = StateGraph(DecisionState)
    
    # Add nodes wrapped in error handlers
    workflow.add_node("ContextIntelligenceAgent", safe_agent_wrapper(context_agent))
    workflow.add_node("RiskInterpretationAgent", safe_agent_wrapper(interpretation_agent))
    workflow.add_node("PolicyAgent", safe_agent_wrapper(policy_agent))
    workflow.add_node("ConversationOrchestrator", safe_agent_wrapper(conversation_agent))
    workflow.add_node("DecisionResolutionEngine", safe_agent_wrapper(decision_engine))
    workflow.add_node("ActionExecutor", safe_agent_wrapper(action_executor))
    workflow.add_node("AuditLogger", safe_agent_wrapper(audit_logger))
    workflow.add_node("MemoryAgent", safe_agent_wrapper(memory_agent))
    workflow.add_node("HumanApproval", human_approval_node)
    
    # Set Entry Point
    workflow.set_entry_point("ContextIntelligenceAgent")
    
    # Dynamic routing
    workflow.add_conditional_edges("ContextIntelligenceAgent", route_next)
    workflow.add_conditional_edges("RiskInterpretationAgent", route_next)
    workflow.add_conditional_edges("PolicyAgent", route_next)
    workflow.add_conditional_edges("ConversationOrchestrator", route_next)
    workflow.add_conditional_edges("DecisionResolutionEngine", route_next)
    workflow.add_conditional_edges("ActionExecutor", route_next)
    workflow.add_conditional_edges("AuditLogger", route_next)
    workflow.add_conditional_edges("HumanApproval", route_next)
    workflow.add_conditional_edges("MemoryAgent", route_next)
    
    # Compile with memory checkpointing to support interrupts
    checkpointer = MemorySaver()
    
    return workflow.compile(
        checkpointer=checkpointer,
        interrupt_before=["HumanApproval"]
    )

decision_graph = create_decision_graph()
