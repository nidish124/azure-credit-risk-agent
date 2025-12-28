from graph.builder import build_credit_decision_graph
from contracts.credit_application import CreditApplication
from contracts.graph_state import CreditDecisionGraphState

def test_graph_executes_end_to_end():
    app = CreditApplication(
        application_id="APP-GRAPH-1",
        applicant_id="CUST-GRAPH",
        employment_type="SALARIED",
        monthly_income=100000,
        existing_emi=30000,
        credit_score=740,
        loan_amount=600000,
        loan_tenure_months=36,
        product_type="PERSONAL_LOAN",
        channel="DIGITAL",
        declared_assets_value=900000
    )

    graph = build_credit_decision_graph()
    final_state = graph.invoke(CreditDecisionGraphState(application=app))

    print(final_state)

    assert final_state.get("risk_output") is not None
    assert final_state.get("policy_output") is not None
    assert final_state.get("decision_output") is not None