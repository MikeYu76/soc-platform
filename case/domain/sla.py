from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class CaseSLA(BaseModel):
    target_minutes: int

    due_at: datetime

    breached: bool = False

    breached_at: datetime | None = None