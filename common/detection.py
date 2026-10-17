from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from common.event import Event


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Detection(BaseModel):
    """
    Represents a security detection produced by a detection rule.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()),
    )

    rule_id: str
    title: str
    severity: Severity
    event: Event

    matched_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )
