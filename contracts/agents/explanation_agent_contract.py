from pydantic import BaseModel
from contracts.explanation_output import ExplanationOutput
from contracts.risk_output import RiskEvaluationOutput
from contracts.policy_output import PolicyEvaluationOutput


class ExplanationAgentInput(BaseModel):
    risk_output: RiskEvaluationOutput
    policy_output: PolicyEvaluationOutput

class ExplanationAgentOutput(ExplanationOutput):
    """
    Inherits:
    - summary
    - key_reasons
    """
    pass
