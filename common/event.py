from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, IPvAnyAddress
from common.event_types import EventType

from uuid import uuid4


class Event(BaseModel):
    """Canonical normalized security event."""

    # Required
    # Required
    timestamp: datetime
    log_source: str
    event_type: EventType
    message: str
    raw_message: str

    # Internal immutable entity identity
    id: str = Field(
        default_factory=lambda: str(uuid4()),
    )

    hostname: str | None = None
    username: str | None = None

    source_ip: IPvAnyAddress | None = None
    destination_ip: IPvAnyAddress | None = None

    # Native event identifier from the source system
    event_id: str | int | None = None

    process_name: str | None = None
    command_line: str | None = None

    