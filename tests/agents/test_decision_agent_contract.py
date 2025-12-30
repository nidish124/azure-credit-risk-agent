from contracts.risk_output import RiskEvaluationOutput, RiskFactor
from contracts.policy_output import PolicyEvaluationOutput
from contracts.agents.decision_agent_contract import DecisionAgentInput
from contracts.credit_application import CreditApplication

def test_decision_agent_input_contract():
    application = CreditApplication(
        application_id="app-10",
        applicant_id="cust-10",
        employment_type="SALARIED",
        monthly_income=90000,
        existing_emi=30000,
        credit_score=730,
        loan_amount=600000,
        loan_tenure_months=36,
        product_type="PERSONAL_LOAN",
        channel="DIGITAL",
        declared_assets_value=800000
    )

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
    policy_output = policy_output, application = application)

    assert inp.risk_output.risk_band == "MEDIUM"
    assert inp.policy_output.policy_status == "PASS"