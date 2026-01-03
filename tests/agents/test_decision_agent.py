from agents.decision_agent import DecisionSynthesisAgent
from contracts.agents.decision_agent_contract import DecisionAgentInput
from contracts.risk_output import RiskEvaluationOutput, RiskBand
from contracts.policy_output import PolicyEvaluationOutput, PolicyStatus
from contracts.credit_application import CreditApplication

def make_input(risk_band, policy_status, hard_stop=False, conditions=None):
    return DecisionAgentInput(
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
        ),
        
        risk_output=RiskEvaluationOutput(
            risk_band=risk_band,
            risk_factors=[],
            data_quality_issues=[],
            max_eligibility_loan_amount = 80000
        ),
        policy_output=PolicyEvaluationOutput(
            policy_status=policy_status,
            conditions=conditions or [],
            hard_stop=hard_stop,
            policy_references=["TEST-POL"]
        )
    )

def test_hard_stop_reject():
    print(make_input("LOW", "PASS", hard_stop=True))
    agent = DecisionSynthesisAgent()
    output = agent.run(make_input("LOW", "PASS", hard_stop=True))
    assert output.recommendation == "REJECT"


def test_conditional_approval():
    agent = DecisionSynthesisAgent()
    output = agent.run(make_input("MEDIUM", "CONDITIONAL", conditions=["ADD_GUARANTOR"]))
    assert output.recommendation == "CONDITIONAL_APPROVE"
    assert "ADD_GUARANTOR" in output.required_actions


def test_low_risk_pass_approve():
    agent = DecisionSynthesisAgent()
    output = agent.run(make_input("LOW", "PASS"))
    assert output.recommendation == "APPROVE"


def test_high_risk_manual_review():
    agent = DecisionSynthesisAgent()
    output = agent.run(make_input("HIGH", "PASS"))
    assert output.recommendation == "MANUAL_REVIEW"
