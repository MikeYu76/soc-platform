from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from common.detection import Detection
from infrastructure.sqlite.mappers.base_mapper import BaseMapper


class DetectionMapper(BaseMapper):
    """
    Maps Detection aggregates to and from persistence records.
    """

    @classmethod
    def to_record(
        cls,
        detection: Detection,
    ) -> dict[str, Any]:
        return {
            "id": detection.id,
            "rule_id": detection.rule_id,
            "severity": detection.severity.value,
            "matched_at": detection.matched_at.isoformat(),
            "data": cls.serialize(detection),
        }

    @classmethod
    def from_record(
        cls,
        record: Mapping[str, Any],
    ) -> Detection:
        return cls.deserialize(
            Detection,
            record["data"],
        )
