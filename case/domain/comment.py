from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CaseComment(BaseModel):
    comment_id: UUID = Field(default_factory=uuid4)

    author: str

    message: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )