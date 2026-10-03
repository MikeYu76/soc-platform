from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, IPvAnyAddress


class Event(BaseModel):
    """Canonical normalized security event."""

    # Required
    timestamp: datetime
    log_source: str
    event_type: str
    message: str
    raw_message: str

    # Optional
    hostname: str | None = None
    username: str | None = None

    source_ip: IPvAnyAddress | None = None
    destination_ip: IPvAnyAddress | None = None

    event_id: str | int | None = None

    process_name: str | None = None
    command_line: str | None = None

    vendor_fields: dict[str, Any] = Field(default_factory=dict)