from contracts.graph_state import CreditDecisionGraphState
from contracts.risk_output import RiskEvaluationOutput, RiskBand
from contracts.policy_output import PolicyEvaluationOutput, PolicyStatus
from contracts.explanation_output import ExplanationOutput
from contracts.decision_output import DecisionOutput, DecisionRecommendation

def risk_node(state: CreditDecisionGraphState) -> CreditDecisionGraphState:
    state.risk_output = RiskEvaluationOutput(
        risk_band=RiskBand.MEDIUM,
        risk_factors=[
            {"factor": "DEBT_TO_INCOME", "impact": "HIGH"},
            {"factor": "CREDIT_SCORE", "impact": "MEDIUM"}
        ],
        data_quality_issues=[]
    )
    return state


from agents.policy_agent import PolicyInterpretationAgent
from api.factories import get_llm, get_policy_search_client
from contracts.agents.policy_agent_contract import PolicyAgentInput

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
    state.explanation_output = ExplanationOutput(
        summary="Moderate risk due to high debt-to-income ratio.",
        key_reasons=[
            "Debt-to-income ratio exceeds preferred threshold",
            "Credit score meets minimum eligibility"
        ],
        risk_references=["DEBT_TO_INCOME", "CREDIT_SCORE"],
        policy_references=state.policy_output.policy_references
    )
    return state

def decision_node(state: CreditDecisionGraphState) -> CreditDecisionGraphState:
    if state.policy_output.hard_stop:
        state.decision_output = DecisionOutput(
            recommendation=DecisionRecommendation.REJECT,
            required_actions=[],
            confidence=0.95
        )
    else:
        state.decision_output = DecisionOutput(
            recommendation=DecisionRecommendation.CONDITIONAL_APPROVE,
            required_actions=state.policy_output.conditions,
            confidence=0.77
        )
    return state