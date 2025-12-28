from enum import Enum
from pydantic import BaseModel, Field, PositiveInt, model_validator
from typing import Optional


class EmploymentType(str, Enum):
    SALARIED = "SALARIED"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    CONTRACTOR = "CONTRACTOR"


class LoanProductType(str, Enum):
    PERSONAL_LOAN = "PERSONAL_LOAN"
    HOME_LOAN = "HOME_LOAN"
    AUTO_LOAN = "AUTO_LOAN"


class ApplicationChannel(str, Enum):
    DIGITAL = "DIGITAL"
    BRANCH = "BRANCH"
    PARTNER = "PARTNER"


class CreditApplication(BaseModel):
    application_id: str = Field(..., description="Unique loan application ID")
    applicant_id: str = Field(..., description="Internal applicant reference ID")

    employment_type: EmploymentType
    monthly_income: PositiveInt = Field(..., description="Monthly income in INR")
    existing_emi: PositiveInt = Field(..., description="Total existing EMI obligations")

    credit_score: PositiveInt = Field(..., ge=300, le=900)

    loan_amount: PositiveInt
    loan_tenure_months: PositiveInt
    product_type: LoanProductType

    channel: ApplicationChannel

    declared_assets_value: PositiveInt = Field(..., description="Total value of assets declared by the applicant.")