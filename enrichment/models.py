from typing import Any

from pydantic import BaseModel, Field

from common.detection import Detection


class Enrichment(BaseModel):
    """Contextual information added to a detection."""

    data: dict[str, Any] = Field(default_factory=dict)


class EnrichedDetection(BaseModel):
    """A detection combined with its enrichment data."""

    detection: Detection
    enrichment: Enrichment
