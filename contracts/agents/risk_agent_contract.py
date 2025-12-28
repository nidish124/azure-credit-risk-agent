from pydantic import BaseModel, Field
from contracts.credit_application import CreditApplication
from contracts.risk_output import RiskEvaluationOutput

class RiskAgentInput(BaseModel):
    application: CreditApplication

class RiskAgentOutput(RiskEvaluationOutput):
    """
    Inherits:
    - risk_band
    - risk_factors
    - data_quality_issues
    """
    
    pass
