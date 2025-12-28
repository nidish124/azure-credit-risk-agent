from contracts.graph_state import CreditDecisionGraphState
from contracts.credit_application import CreditApplication


def test_graph_state_initialization():
    app = CreditApplication(
        application_id="APP-004",
        applicant_id="CUST-456",
        employment_type="SALARIED",
        monthly_income=100000,
        existing_emi=30000,
        credit_score=760,
        loan_amount=800000,
        loan_tenure_months=36,
        product_type="PERSONAL_LOAN",
        channel="BRANCH",
        declared_assets_value = 1800000
    )

    state = CreditDecisionGraphState(application=app)

    assert state.application.application_id == "APP-004"
    assert state.decision_output is None
