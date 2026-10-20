from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.dto.base import Response


@dataclass(slots=True)
class GetEventIndexOutboxStatusResponse(Response):
    """Operational status for the OpenSearch indexing queue."""

    enabled: bool
    pending_count: int
    ready_count: int
    retry_wait_count: int
    retrying_count: int
    oldest_pending_at: datetime | None
    oldest_pending_age_seconds: float | None
    max_attempts: int
