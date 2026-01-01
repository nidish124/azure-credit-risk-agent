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
        llm = get_llm(token_tracker=state.token_tracker, agent_name="risk_agent"),
        prompt_template=open("agents/prompts/risk_prompt.txt").read()
    )
    input_data = RiskAgentInput(application=state.application)

    state.token_tracker.record(
        agent_name="risk_agent",
        text=input_data.model_dump_json()
    )
    state.risk_output = agent.run(input_data)

    state.token_tracker.record(
        agent_name="risk_agent",
        text=state.risk_output.model_dump_json()
    )

    return state

def policy_node(state: CreditDecisionGraphState) -> CreditDecisionGraphState:
    agent = PolicyInterpretationAgent(
        llm=get_llm( token_tracker=state.token_tracker, agent_name="policy_agent"),
        search_client=get_policy_search_client(),
        prompt_template=open("agents/prompts/policy_prompt.txt").read()
    )
    
    input_data = PolicyAgentInput(
        application=state.application,
        risk_output=state.risk_output
    )

    state.token_tracker.record(
        agent_name="policy_agent",
        text=input_data.model_dump_json()
    )
    
    state.policy_output = agent.run(input_data)

    state.token_tracker.record(
        agent_name="policy_agent",
        text=state.policy_output.model_dump_json()
    )
    return state

def explanation_node(state: CreditDecisionGraphState) -> CreditDecisionGraphState:
    agent = ExplainabilityAgent(
        llm = get_llm(token_tracker=state.token_tracker, agent_name="explanation_agent"), 
        prompt_template=open("agents/prompts/explanation_prompt.txt").read()
    )
    input_data = ExplanationAgentInput(
        risk_output=state.risk_output,
        policy_output=state.policy_output
    )
    state.token_tracker.record(
        agent_name="explanation_agent",
        text=input_data.model_dump_json()
    )
    state.explanation_output = agent.run(input_data)

    state.token_tracker.record(
        agent_name="explanation_agent",
        text=state.explanation_output.model_dump_json()
    )
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

