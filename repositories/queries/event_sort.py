from __future__ import annotations

from enum import StrEnum


class EventSort(StrEnum):
    """
    Supported event sort fields.
    """

    TIMESTAMP = "timestamp"
    HOSTNAME = "hostname"
    USERNAME = "username"
    EVENT_TYPE = "event_type"
