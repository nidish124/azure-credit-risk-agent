from agents.ollama_provider import OllamaProvider
from agents.risk_agent import RiskScoringAgent
from agents.policy_agent import PolicyInterpretationAgent
from agents.explanation_agent import ExplainabilityAgent
from agents.decision_agent import DecisionSynthesisAgent
from graph.builder import build_credit_decision_graph
from api.factories import get_llm, get_policy_search_client

def get_graph():
    return build_credit_decision_graph()

