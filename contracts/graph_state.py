from pydantic import BaseModel
from typing import Optional

from contracts.credit_application import CreditApplication
from contracts.risk_output import RiskEvaluationOutput
from contracts.policy_output import PolicyEvaluationOutput
from contracts.explanation_output import ExplanationOutput
from contracts.decision_output import DecisionOutput


class CreditDecisionGraphState(BaseModel):
    application: CreditApplication

    risk_output: Optional[RiskEvaluationOutput] = None
    policy_output: Optional[PolicyEvaluationOutput] = None
    explanation_output: Optional[ExplanationOutput] = None
    decision_output: Optional[DecisionOutput] = None

    error: Optional[str] = None
