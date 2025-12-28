import pytest
from pydantic import ValidationError
from contracts.credit_application import CreditApplication


def test_valid_credit_application():
    app = CreditApplication(
        application_id="APP-001",
        applicant_id="CUST-123",
        employment_type="SALARIED",
        monthly_income=95000,
        existing_emi=32000,
        credit_score=742,
        loan_amount=1200000,
        loan_tenure_months=48,
        product_type="PERSONAL_LOAN",
        channel="DIGITAL",
        declared_assets_value = 1900000
    )

    assert app.credit_score == 742
    assert app.monthly_income > app.existing_emi


def test_invalid_employment_type_fails():
    with pytest.raises(ValidationError):
        CreditApplication(
            application_id="APP-002",
            applicant_id="CUST-999",
            employment_type="FREELANCER",  # ❌ invalid
            monthly_income=80000,
            existing_emi=20000,
            credit_score=720,
            loan_amount=500000,
            loan_tenure_months=36,
            product_type="PERSONAL_LOAN",
            channel="DIGITAL",
            declared_assets_value = 700000
        )


def test_credit_score_out_of_range_fails():
    with pytest.raises(ValidationError):
        CreditApplication(
            application_id="APP-003",
            applicant_id="CUST-888",
            employment_type="SALARIED",
            monthly_income=80000,
            existing_emi=20000,
            credit_score=950,  # ❌ invalid
            loan_amount=500000,
            loan_tenure_months=36,
            product_type="PERSONAL_LOAN",
            channel="DIGITAL",
            declared_assets_value = 100000
        )
