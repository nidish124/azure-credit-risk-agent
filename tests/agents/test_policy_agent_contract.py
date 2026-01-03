from contracts.credit_application import CreditApplication
from contracts.policy_output import PolicyEvaluationOutput
from contracts.risk_output import RiskEvaluationOutput
from contracts.agents.policy_agent_contract import PolicyAgentInput

def test_policy_agent_input_contract():
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

    risk_inp = RiskEvaluationOutput(
        risk_band="LOW",
        risk_factors=[],
        max_eligibility_loan_amount=60000
    )

    inp = PolicyAgentInput(application=application, risk_output=risk_inp)

    assert inp.application.monthly_income == 90000
    assert inp.risk_output.risk_band == "LOW"