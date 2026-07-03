import os
import sys
import logging
import json
from dotenv import load_dotenv

# Ensure the project root is in the python path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

from ai.orchestrator.graph import decision_graph
from ai.schemas.conversation import ConversationMessage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def run_scenario(transaction_data: dict, customer_id: int):
    # Initialize the state
    initial_state = {
        "transaction_id": transaction_data.get("transaction_id"),
        "raw_transaction_data": transaction_data,
        "raw_customer_id": customer_id,
        "audit_trail": [],
        "errors": [],
        "messages": [],
        "workflow_status": "RUNNING"
    }
    
    config = {"configurable": {"thread_id": transaction_data.get("transaction_id", "demo-thread")}}
    
    print("\n" + "="*50)
    print(f"Starting Scenario for Tx: {transaction_data.get('transaction_id')}")
    print("="*50)
    
    # Run the graph until it pauses or finishes
    for event in decision_graph.stream(initial_state, config=config):
        for key, value in event.items():
            if key == "ContextIntelligenceAgent":
                context = value.get("context")
                if context:
                    print(f"\n--- Output from ContextIntelligenceAgent ---")
                    print(f"Context Normalized: User {context['customer']['user_id']} - Risk: {context['ml_risk']['risk_score']}")
            elif key == "RiskInterpretationAgent":
                evidence = value.get("evidence")
                print(f"\n--- Output from RiskInterpretationAgent ---")
                if evidence:
                    print(f"Evidence: {evidence['overall_summary']}")
                else:
                    print("Evidence Report failed to generate.")
            elif key == "PolicyAgent":
                policy = value.get("policy_decision")
                print(f"\n--- Output from PolicyAgent ---")
                if policy:
                    print(f"Policy Action: {policy['action']}")
                else:
                    print("Policy Decision failed.")
            elif key == "ConversationOrchestrator":
                action = value.get("last_action")
                print(f"\n--- Output from ConversationOrchestrator ---")
                if action:
                    print(f"Agent to Customer: {action['message_to_customer']}")
                    if action.get('requires_response'):
                        print(f"--> [Awaiting Customer Response]")
                else:
                    print("Conversation Action failed.")
            elif key == "DecisionResolutionEngine":
                pass # Decision logic runs silently, results caught by logger
            elif key == "ActionExecutor":
                pass # ActionExecutor prints its own logs
            elif key == "AuditLogger":
                pass # AuditLogger prints its own logs
            elif key == "MemoryAgent":
                print("\n--- Output from MemoryAgent ---")
                print("Memory updated successfully.")
    
    state = decision_graph.get_state(config)
    
    # Handle Human-in-the-Loop Interrupt
    while state.next and state.next[0] == "HumanApproval":
        customer_input = input("\n[Customer Input]: ")
        
        # Correct LangGraph Resume Logic
        # We update the state in the "HumanApproval" node, then stream again with NO input to resume.
        new_msg = {"role": "user", "content": customer_input}
        decision_graph.update_state(
            config, 
            {
                "messages": [new_msg],
                "next_agent": "ConversationOrchestrator",
                "workflow_status": "RUNNING"
            }, 
            as_node="HumanApproval"
        )
        
        for event in decision_graph.stream(None, config=config):
            for key, value in event.items():
                if key == "ConversationOrchestrator":
                    action = value.get("last_action")
                    print(f"\n--- Output from ConversationOrchestrator ---")
                    if action:
                        print(f"Agent to Customer: {action['message_to_customer']}")
                        if action.get('requires_response'):
                            print(f"--> [Awaiting Customer Response]")
                elif key == "DecisionResolutionEngine":
                    pass
                elif key == "ActionExecutor":
                    pass
                elif key == "AuditLogger":
                    pass
                elif key == "MemoryAgent":
                    print("\n--- Output from MemoryAgent ---")
                    print("Memory updated successfully.")
                elif key == "HumanApproval":
                    pass
                    
        state = decision_graph.get_state(config)
                    
    final_state = state.values
    
    # The Decision Trace is now handled natively by the AuditLogger node.
    # Calculate Observability
    print("\n" + "="*48)
    print("Performance Dashboard")
    print("="*48)
    
    audit_trail = final_state.get("audit_trail", [])
    total_time = 0.0
    
    for record in audit_trail:
        action = record.get("agent", "")
        duration = record.get("duration_seconds", 0)
        total_time += duration
        print(f"{action.ljust(25)} : {duration:.3f}s")
        
    print("-" * 48)
    print(f"Total Workflow Time       : {total_time:.3f}s")
    print("================================================")

    
def get_demo_scenarios():
    import random
    uid = random.randint(1000, 9999)
    
    base_tx = {
        "amount": 150.0,
        "currency": "USD",
        "type": "TRANSFER",
        "recipient_id": 100,
        "recipient_name": "Amazon",
        "average_transaction": 120.0,
        "current_balance": 5000.0,
        "timestamp": "2026-07-02 23:30:00",
        "trusted_recipient": True,
        "transaction_count": 50,
        "trust_score": 95,
        "reported_scam_count_rep": 0,
        "favorite_categories": "Shopping, Utilities",
        "category": "Shopping",
        "usual_location": "New York",
        "city": "New York",
        "usual_device": "iPhone",
        "device_type": "iPhone",
        "risk_profile": "Low",
        "digital_payment_ratio": 0.8,
        "transaction_type": "TRANSFER",
        "payment_channel": "MOBILE"
    }

    scenarios = {
        "1": ("Normal Transfer", {**base_tx, "transaction_id": f"TX-NORM-{uid}", "amount": 45.0, "recipient_name": "Netflix", "category": "Entertainment"}),
        "2": ("Crypto Scam", {**base_tx, "transaction_id": f"TX-CRYPTO-{uid}", "amount": 15000.0, "recipient_name": "Coinbase Exchange", "trusted_recipient": False, "category": "Investment", "usual_device": "iPhone", "device_type": "Android", "city": "Unknown IP"}),
        "3": ("Investment Scam", {**base_tx, "transaction_id": f"TX-INV-{uid}", "amount": 50000.0, "recipient_name": "Alpha Traders Ltd", "trusted_recipient": False, "reported_scam_count_rep": 3}),
        "4": ("Romance Scam", {**base_tx, "transaction_id": f"TX-ROM-{uid}", "amount": 5000.0, "recipient_name": "John Doe", "trusted_recipient": False, "transaction_count": 0, "trust_score": 10}),
        "5": ("Fake Bank Officer", {**base_tx, "transaction_id": f"TX-OFF-{uid}", "amount": 9000.0, "recipient_name": "Safe Account 101", "trusted_recipient": False, "type": "WIRE"}),
        "6": ("Deepfake Scam", {**base_tx, "transaction_id": f"TX-DEEP-{uid}", "amount": 25000.0, "recipient_name": "CEO Emergency Fund", "trusted_recipient": False}),
        "7": ("Lottery Scam", {**base_tx, "transaction_id": f"TX-LOT-{uid}", "amount": 1000.0, "recipient_name": "Global Winners LLC", "trusted_recipient": False, "category": "Fees"}),
        "8": ("Emergency Relative Scam", {**base_tx, "transaction_id": f"TX-EMERG-{uid}", "amount": 3000.0, "recipient_name": "Bail Bonds Inc", "trusted_recipient": False}),
        "9": ("Custom Scenario", {**base_tx, "transaction_id": f"TX-CUST-{uid}"}),
    }
    return scenarios

if __name__ == "__main__":
    load_dotenv()
    
    scenarios = get_demo_scenarios()
    
    print("\n" + "="*50)
    print("NIRNAY - Agentic AI Decision Intelligence Platform")
    print("==================================================")
    for key, (name, _) in scenarios.items():
        print(f"[{key}] {name}")
    print("="*50)
    
    choice = input("\nChoose Scenario (1-9): ").strip()
    
    if choice in scenarios:
        name, tx_data = scenarios[choice]
        print(f"\nLoading Scenario: {name}...")
        run_scenario(tx_data, customer_id=1)
    else:
        print("Invalid choice. Exiting.")
