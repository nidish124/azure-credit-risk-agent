from pydantic import BaseModel
from contracts.decision_output import DecisionOutput
from contracts.risk_output import RiskEvaluationOutput
from contracts.policy_output import PolicyEvaluationOutput


class DecisionAgentInput(BaseModel):
    risk_output: RiskEvaluationOutput
    policy_output: PolicyEvaluationOutput

class DecisionAgentOutput(DecisionOutput):
    """
    Inherits:
    - recommendation
    - required_actions
    - confidence
    - human_approval_required
    """
    pass
