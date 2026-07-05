from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

from backend.app.models.user import User
from backend.app.models.transaction import Transaction, TransactionState
from backend.app.database.session import get_db
from backend.app.api.dependencies import get_current_user
from backend.app.services.transaction_orchestrator import TransactionOrchestrator
from backend.app.repositories.transaction_repo import transaction_repo
from ai.orchestrator.graph import decision_graph

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str
    transactionId: str

class ChatResponse(BaseModel):
    message: str
    status: str
    decision: Optional[str] = None
    conversation_history: List[Dict[str, Any]] = []

@router.post('/chat', response_model=ChatResponse)
def handle_conversation_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        tx_id = int(request.transactionId)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid transaction ID format")
        
    transaction = transaction_repo.get(db, id=tx_id)
    if not transaction or transaction.account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    if transaction.status not in [TransactionState.AWAITING_CUSTOMER_RESPONSE, TransactionState.PENDING_DECISION]:
        return ChatResponse(
            message=f"This transaction is already in state: {transaction.status}",
            status="COMPLETED",
            decision=str(transaction.status)
        )
        
    config = {"configurable": {"thread_id": str(transaction.id)}}
    state = decision_graph.get_state(config)
    
    if not state.values:
        raise HTTPException(status_code=400, detail="No active decision session found for this transaction")
        
    messages = list(state.values.get("messages", []))
    new_msg = {"role": "user", "content": request.message}
    messages.append(new_msg)
    
    decision_graph.update_state(
        config,
        {
            "messages": messages,
            "next_agent": "ConversationOrchestrator",
            "workflow_status": "RUNNING"
        },
        as_node="HumanApproval"
    )
    
    try:
        for event in decision_graph.stream(None, config=config):
            pass
    except Exception as e:
        logger.error(f"LangGraph resume streaming failed: {e}")
        
    updated_state = decision_graph.get_state(config)
    values = updated_state.values
    
    last_action = values.get("last_action", {})
    decision_result = values.get("decision_result", {})
    workflow_status = values.get("workflow_status", "RUNNING")
    
    response_msg = last_action.get("message_to_customer", "Processing your response...")
    requires_response = last_action.get("requires_response", True)
    
    final_decision = None
    if workflow_status == "COMPLETED" or not requires_response:
        final_decision = decision_result.get("final_decision", "APPROVE_TRANSACTION")
        
        if final_decision == "APPROVE_TRANSACTION":
            TransactionOrchestrator._update_state(db, transaction, TransactionState.STEP_UP_AUTHENTICATION)
        elif final_decision == "CANCEL_TRANSACTION":
            TransactionOrchestrator._update_state(db, transaction, TransactionState.FAILED)
        else:
            TransactionOrchestrator._update_state(db, transaction, TransactionState.BLOCKED)
            
        if transaction.risk_event:
            transaction.risk_event.recommended_action = final_decision
            transaction.risk_event.reason_codes = [decision_result.get("decision_reason", "AI Decision")]
            db.commit()
            
    return ChatResponse(
        message=response_msg,
        status="AWAITING_RESPONSE" if requires_response and workflow_status != "COMPLETED" else "COMPLETED",
        decision=final_decision,
        conversation_history=values.get("messages", [])
    )
