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
            "id": event.id,
            "timestamp": event.timestamp.isoformat(),
            "log_source": event.log_source,
            "event_type": event.event_type.value,
            "hostname": event.hostname,
            "username": event.username,
            "source_ip": (
                str(event.source_ip) if event.source_ip is not None else None
            ),
            "destination_ip": (
                str(event.destination_ip)
                if event.destination_ip is not None
                else None
            ),
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
