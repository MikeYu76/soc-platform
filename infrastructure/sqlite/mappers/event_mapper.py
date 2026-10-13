from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from common.event import Event

from infrastructure.sqlite.mappers.base_mapper import BaseMapper


class EventMapper(BaseMapper):
    """
    Maps Event models to and from persistence records.
    """

    @classmethod
    def to_record(
        cls,
        event: Event,
    ) -> dict[str, Any]:
        return {
            "id": str(event.event_id),
            "timestamp": event.timestamp.isoformat(),
            "log_source": event.log_source,
            "event_type": event.event_type.value,
            "data": cls.serialize(event),
        }

    @classmethod
    def from_record(
        cls,
        record: Mapping[str, Any],
    ) -> Event:
        return cls.deserialize(
            Event,
            record["data"],
        )