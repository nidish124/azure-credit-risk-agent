from contracts.risk_output import RiskEvaluationOutput, RiskFactor


def test_valid_risk_output():
    risk = RiskEvaluationOutput(
        risk_band="MEDIUM",
        risk_factors=[
            RiskFactor(factor="DEBT_TO_INCOME", impact="HIGH"),
            RiskFactor(factor="CREDIT_SCORE", impact="MEDIUM")
        ],
        max_eligibility_loan_amount=60000
    )

    assert risk.risk_band == "MEDIUM"
    assert len(risk.risk_factors) == 2
