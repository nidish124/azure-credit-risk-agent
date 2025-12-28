from pydantic import BaseModel
from contracts.credit_application import CreditApplication
from contracts.policy_output import PolicyEvaluationOutput
from contracts.risk_output import RiskEvaluationOutput

class PolicyAgentInput(BaseModel):
    application: CreditApplication
    risk_output: RiskEvaluationOutput

class PolicyAgentOutput(PolicyEvaluationOutput):
    """
    Inherits:
    - policy_status
    - conditions
    - hard_stop
    - policy_references
    """
    pass