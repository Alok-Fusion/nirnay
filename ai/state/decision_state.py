import operator
from typing import TypedDict, Annotated, Sequence, Optional, List, Dict, Any
from ai.schemas.context import DecisionContext
from ai.schemas.interpretation import EvidenceReport
from ai.schemas.policy import PolicyDecision
from ai.schemas.conversation import ConversationMessage, ConversationAction, ConversationState
from ai.schemas.decision import DecisionResult

class DecisionState(TypedDict):
    """The central state maintained by the LangGraph orchestrator."""
    transaction_id: str
    case_id: Optional[str]
    
    # Inputs
    raw_transaction_data: Dict[str, Any]
    raw_customer_id: int
    
    # Context (Agent 1)
    context: Optional[DecisionContext]
    
    # Interpretation (Agent 2)
    evidence: Optional[EvidenceReport]
    
    # Policy (Agent 3)
    policy_decision: Optional[PolicyDecision]
    
    # Conversation (Agent 4)
    messages: Annotated[Sequence[Dict[str, str]], operator.add]
    last_action: Optional[ConversationAction]
    conversation_state: Optional[Dict[str, Any]]
    
    # Decision Engine
    decision_result: Optional[Dict[str, Any]]
    
    # Memory (Agent 5)
    memory_context: Optional[Dict[str, Any]]
    
    # Workflow control
    current_agent: str
    next_agent: str
    workflow_status: str # "RUNNING", "AWAITING_CUSTOMER", "COMPLETED", "FAILED"
    
    # Tracing / Observability
    audit_trail: Annotated[Sequence[Dict[str, Any]], operator.add]
    errors: Annotated[Sequence[str], operator.add]
