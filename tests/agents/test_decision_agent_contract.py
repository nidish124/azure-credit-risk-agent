from contracts.decision_output import DecisionOutput
from contracts.risk_output import RiskEvaluationOutput, RiskFactor
from contracts.policy_output import PolicyEvaluationOutput
from contracts.agents.decision_agent_contract import DecisionAgentInput

def test_decision_agent_input_contract():
    policy_output = PolicyEvaluationOutput(
        policy_status="PASS",
        conditions=[],
        hard_stop=False,
        policy_references=["CREDIT-POL-4.1"]
    )
    risk_output = RiskEvaluationOutput(
        risk_band="MEDIUM",
        risk_factors=[
            RiskFactor(factor="DEBT_TO_INCOME", impact="HIGH"),
            RiskFactor(factor="CREDIT_SCORE", impact="MEDIUM")
        ]
    )
    
    inp = DecisionAgentInput(risk_output = risk_output,
    policy_output = policy_output)

    assert inp.risk_output.risk_band == "MEDIUM"
    assert inp.policy_output.policy_status == "PASS"