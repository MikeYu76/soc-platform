from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from alert.models import Alert

from infrastructure.sqlite.mappers.base_mapper import BaseMapper


class AlertMapper(BaseMapper):
    """
    Maps Alert aggregates to and from persistence records.
    """

    @classmethod
    def to_record(
        cls,
        alert: Alert,
    ) -> dict[str, Any]:
        return {
            "id": str(alert.alert_id),
            "status": alert.status.value,
            "severity": alert.severity.value,
            "created_at": alert.created_at.isoformat(),
            "data": cls.serialize(alert),
        }

    @classmethod
    def from_record(
        cls,
        record: dict[str, Any],
    ) -> Alert:
        return cls.deserialize(
            Alert,
            record["data"],
        )