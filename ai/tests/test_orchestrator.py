import pytest
from ai.orchestrator.graph import decision_graph

def test_decision_graph_compiles():
    """Verify that the StateGraph is properly formed and compiles."""
    assert decision_graph is not None
    # We can check the nodes
    nodes = list(decision_graph.nodes.keys())
    assert "ContextIntelligenceAgent" in nodes
    assert "RiskInterpretationAgent" in nodes
    assert "PolicyAgent" in nodes
    assert "ConversationOrchestrator" in nodes
    assert "MemoryAgent" in nodes
    assert "HumanApproval" in nodes
