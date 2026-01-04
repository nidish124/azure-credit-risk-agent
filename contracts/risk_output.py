from enum import Enum
from pydantic import BaseModel, Field
from typing import List


class RiskBand(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RiskFactor(BaseModel):
    factor: str = Field(..., description="Risk factor name")
    impact: str = Field(..., description="LOW / MEDIUM / HIGH impact")


class RiskEvaluationOutput(BaseModel):
    risk_band: RiskBand
    risk_factors: List[RiskFactor]

    data_quality_issues: List[str] = Field(
        default_factory=list,
        description="Missing or suspicious data flags"
    )

