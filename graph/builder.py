from langgraph.graph import StateGraph, END
from contracts.graph_state import CreditDecisionGraphState
from graph.nodes import (
    risk_node,
    policy_node,
    explanation_node,
    decision_node,)
from graph.conditions import policy_hard_stop

def build_credit_decision_graph():
    graph = StateGraph(CreditDecisionGraphState)

    graph.add_node("risk", risk_node)
    graph.add_node("policy", policy_node)
    graph.add_node("explain", explanation_node)
    graph.add_node("decision", decision_node)

    graph.set_entry_point("risk")

    graph.add_edge("risk", "policy")

    graph.add_conditional_edges(
        "policy",
        policy_hard_stop,
        {
            "decision": "decision",
            "explain": "explain",
        }
    )

    graph.add_edge("explain", "decision")
    graph.add_edge("decision", END)

    return graph.compile()
