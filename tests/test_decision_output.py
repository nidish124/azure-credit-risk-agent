import pytest
from pydantic import ValidationError
from contracts.decision_output import DecisionOutput


def test_valid_decision_output():
    decision = DecisionOutput(
        recommendation="CONDITIONAL_APPROVE",
        required_actions=["ADD_GUARANTOR"],
        confidence=0.78

    )

    assert decision.human_approval_required is True
    assert 0.0 <= decision.confidence <= 1.0


def test_invalid_confidence_fails():
    with pytest.raises(ValidationError):
        DecisionOutput(
            recommendation="APPROVE",
            required_actions=[],
            confidence=1.5 # ❌ invalid

        )
