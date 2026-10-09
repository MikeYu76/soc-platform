
from pydantic import BaseModel, Field


class RiskAssessment(BaseModel):
    """A risk score assigned to a detection."""

    detection_id: str
    score: int = Field(ge=0, le=100)
    severity: str
    reasoning: str