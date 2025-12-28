from pydantic import BaseModel, Field
from typing import List


class ExplanationOutput(BaseModel):
    summary: str = Field(..., description="One-line human-readable explanation")

    key_reasons: List[str] = Field(
        ...,
        description="Ranked reasons influencing decision"
    )

    risk_references: List[str] = Field(
        ...,
        description="References to risk factors used"
    )

    policy_references: List[str] = Field(
        ...,
        description="References to policy clauses used"
    )
