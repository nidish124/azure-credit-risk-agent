from enum import Enum
from pydantic import BaseModel, Field
from typing import List


class DecisionRecommendation(str, Enum):
    APPROVE = "APPROVE"
    CONDITIONAL_APPROVE = "CONDITIONAL_APPROVE"
    REJECT = "REJECT"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class DecisionOutput(BaseModel):
    recommendation: DecisionRecommendation

    required_actions: List[str] = Field(
        default_factory=list,
        description="Actions required before approval"
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in recommendation (bounded)"
    )

    human_approval_required: bool = Field(
        default=True,
        description="Explicit human-in-the-loop requirement"
    )
