# NIRNAY - LangGraph Integration Guide

The NIRNAY platform leverages LangGraph to orchestrate a stateful, multi-agent AI workflow.

## The Decision State
All intelligence is persisted and passed through the `DecisionState` TypedDict. It stores:
- **Raw Inputs:** `transaction_id`, `raw_transaction_data`, `raw_customer_id`
- **Context Profiles:** `context` (Feature Engineering & FAISS context)
- **ML Outputs:** `evidence` (LLM-interpreted Risk Scores)
- **Business Logic:** `policy_decision` (Rules, AI Confidence, and Recommendations)
- **Conversational Memory:** `messages` (Continuity layer)
- **Workflow Control:** `workflow_status`, `next_agent`, `current_agent`
- **Observability:** `audit_trail`, `errors`

## State Transitions
State transitions are explicitly managed by the `route_next` conditional edge. 

```python
workflow.add_conditional_edges("ContextIntelligenceAgent", route_next)
workflow.add_conditional_edges("RiskInterpretationAgent", route_next)
workflow.add_conditional_edges("PolicyAgent", route_next)
workflow.add_conditional_edges("ConversationOrchestrator", route_next)
```

## Exception Handling
We implemented a `safe_agent_wrapper` to ensure LangGraph never crashes on Pydantic validation errors or external API timeouts. If an agent fails, it safely transitions to `FAILED` and routes to `END`.

## Human-in-the-Loop Interrupt
When the `PolicyAgent` dictates a transaction is too risky, the `ConversationOrchestrator` generates a dynamic customer prompt and sets `requires_response=True`.
LangGraph safely pauses using `interrupt_before=["HumanApproval"]`. 

When resuming from the CLI Demo:
```python
decision_graph.update_state(
    config, 
    {
        "messages": [new_msg],
        "next_agent": "ConversationOrchestrator",
        "workflow_status": "RUNNING"
    }, 
    as_node="HumanApproval"
)
```
This elegantly simulates an async HTTP API webhook callback from a mobile application.
