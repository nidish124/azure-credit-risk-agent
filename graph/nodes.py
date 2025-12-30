from contracts.graph_state import CreditDecisionGraphState
from contracts.agents.risk_agent_contract import RiskAgentInput
from agents.risk_agent import RiskScoringAgent
from agents.explanation_agent import ExplainabilityAgent
from agents.decision_agent import DecisionSynthesisAgent
from contracts.agents.decision_agent_contract import DecisionAgentInput
from contracts.agents.explanation_agent_contract import ExplanationAgentInput
from agents.policy_agent import PolicyInterpretationAgent
from api.factories import get_llm, get_policy_search_client
from contracts.agents.policy_agent_contract import PolicyAgentInput

def risk_node(state: CreditDecisionGraphState) -> CreditDecisionGraphState:
    agent = RiskScoringAgent(
        llm = get_llm(),
        prompt_template=open("agents/prompts/risk_prompt.txt").read()
    )
    input_data = RiskAgentInput(application=state.application)
    state.risk_output = agent.run(input_data)
    return state

def policy_node(state: CreditDecisionGraphState) -> CreditDecisionGraphState:
    agent = PolicyInterpretationAgent(
        llm=get_llm(),
        search_client=get_policy_search_client(),
        prompt_template=open("agents/prompts/policy_prompt.txt").read()
    )
    
    input_data = PolicyAgentInput(
        application=state.application,
        risk_output=state.risk_output
    )
    
    state.policy_output = agent.run(input_data)
    return state

def explanation_node(state: CreditDecisionGraphState) -> CreditDecisionGraphState:
    agent = ExplainabilityAgent(
        llm = get_llm(),
        prompt_template=open("agents/prompts/explanation_prompt.txt").read()
    )
    input_data = ExplanationAgentInput(
        risk_output=state.risk_output,
        policy_output=state.policy_output
    )
    state.explanation_output = agent.run(input_data)
    return state

def decision_node(state: CreditDecisionGraphState) -> CreditDecisionGraphState:
    agent = DecisionSynthesisAgent()
    input_data = DecisionAgentInput(
        risk_output=state.risk_output,
        policy_output=state.policy_output,
        application=state.application
    )
    state.decision_output = agent.run(input_data)

    return state

