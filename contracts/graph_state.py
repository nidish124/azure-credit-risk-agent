from pydantic import BaseModel,ConfigDict
from typing import Optional

from contracts.credit_application import CreditApplication
from contracts.risk_output import RiskEvaluationOutput
from contracts.policy_output import PolicyEvaluationOutput
from contracts.explanation_output import ExplanationOutput
from contracts.decision_output import DecisionOutput
from infra.token_tracker import TokenTracker

class CreditDecisionGraphState(BaseModel):
    application: CreditApplication

    risk_output: Optional[RiskEvaluationOutput] = None
    policy_output: Optional[PolicyEvaluationOutput] = None
    explanation_output: Optional[ExplanationOutput] = None
    decision_output: Optional[DecisionOutput] = None
    token_tracker: TokenTracker = TokenTracker()
    error: Optional[str] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)