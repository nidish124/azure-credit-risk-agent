from enum import Enum
from pydantic import BaseModel, Field
from typing import List


class PolicyStatus(str, Enum):
    PASS = "PASS"
    CONDITIONAL = "CONDITIONAL"
    FAIL = "FAIL"


class PolicyEvaluationOutput(BaseModel):
    policy_status: PolicyStatus

    conditions: List[str] = Field(
        default_factory=list,
        description="Conditions required to satisfy policy"
    )

    hard_stop: bool = Field(
        ...,
        description="If true, application must be rejected regardless of risk"
    )

    policy_references: List[str] = Field(
        ...,
        description="Policy clause references (e.g., CREDIT-POL-4.2)"
    )
