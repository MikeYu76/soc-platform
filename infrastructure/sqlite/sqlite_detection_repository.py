from __future__ import annotations

from datetime import datetime

from common.detection import Detection, Severity

from infrastructure.sqlite.base_repository import SQLiteRepository
from infrastructure.sqlite.mappers.detection_mapper import (
    DetectionMapper,
)

from repositories.detection_repository import DetectionRepository


class SQLiteDetectionRepository(
    SQLiteRepository,
    DetectionRepository,
):
    """
    SQLite implementation of DetectionRepository.
    """

    TABLE = "detections"

    def save(
        self,
        detection: Detection,
    ) -> None:
        self._upsert(
            table=self.TABLE,
            values=DetectionMapper.to_record(detection),
        )

    def get(
        self,
        detection_id: str,
    ) -> Detection | None:
        row = self._fetch_one(
            """
            SELECT *
            FROM detections
            WHERE id = ?
            """,
            (detection_id,),
        )

        if row is None:
            return None

        return DetectionMapper.from_record(
            self._row_to_dict(row),
        )

    def list_by_rule(
        self,
        rule_id: str,
    ) -> list[Detection]:
        rows = self._fetch_by_column(
            table=self.TABLE,
            column="rule_id",
            value=rule_id,
        )

        return [
            DetectionMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]

    def list_by_severity(
        self,
        severity: Severity,
    ) -> list[Detection]:
        rows = self._fetch_by_column(
            table=self.TABLE,
            column="severity",
            value=severity.value,
        )

        return [
            DetectionMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]

    def list_since(
        self,
        since: datetime,
    ) -> list[Detection]:
        rows = self._fetch_all(
            """
            SELECT *
            FROM detections
            WHERE matched_at >= ?
            ORDER BY matched_at
            """,
            (since.isoformat(),),
        )

        return [
            DetectionMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]