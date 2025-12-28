from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_credit_evaluate_endpoint():
    response = client.post(
        "/credit/evaluate",
        json={
            "application_id": "APP-API-TEST",
            "applicant_id": "CUST-API",
            "employment_type": "SALARIED",
            "monthly_income": 90000,
            "existing_emi": 30000,
            "credit_score": 730,
            "loan_amount": 600000,
            "loan_tenure_months": 36,
            "product_type": "PERSONAL_LOAN",
            "channel": "DIGITAL",
            "declared_assets_value": 800000
        }
    )

    assert response.status_code == 200
    body = response.json()

    assert "decision" in body
    assert "explanation" in body
