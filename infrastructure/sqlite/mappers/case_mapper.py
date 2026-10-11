from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from case.models import Case

from infrastructure.sqlite.mappers.base_mapper import BaseMapper


class CaseMapper(BaseMapper):
    """
    Maps Case aggregates to and from persistence records.
    """

    @classmethod
    def to_record(
        cls,
        case: Case,
    ) -> dict[str, Any]:
        return {
            "id": str(case.case_id),
            "status": case.status.value,
            "priority": case.priority.value,
            "assigned_to": case.assigned_to,
            "created_at": case.created_at.isoformat(),
            "closed_at": (
                case.closed_at.isoformat()
                if case.closed_at is not None
                else None
            ),
            "data": cls.serialize(case),
        }

    @classmethod
    def from_record(
        cls,
        record: Mapping[str, Any],
    ) -> Case:
        return cls.deserialize(
            Case,
            str(record["data"]),
        )