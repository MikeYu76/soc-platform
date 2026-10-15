from __future__ import annotations

from uuid import UUID

from alert.models import Alert

from common.alert_status import AlertStatus
from common.detection import Severity

from infrastructure.sqlite.base_repository import SQLiteRepository
from infrastructure.sqlite.mappers.alert_mapper import AlertMapper

from repositories.alert_repository import AlertRepository


class SQLiteAlertRepository(
    SQLiteRepository,
    AlertRepository,
):
    """
    SQLite implementation of AlertRepository.
    """

    TABLE = "alerts"

    def save(
        self,
        alert: Alert,
    ) -> None:
        self._upsert(
            table=self.TABLE,
            values=AlertMapper.to_record(alert),
        )

    def get(
        self,
        id: UUID,
    ) -> Alert | None:
        row = self._fetch_one(
            """
            SELECT *
            FROM alerts
            WHERE id = ?
            """,
            (str(id),),
        )

        if row is None:
            return None

        return AlertMapper.from_record(
            self._row_to_dict(row),
        )

    def list_active(
        self,
    ) -> list[Alert]:
        rows = self._fetch_all(
            """
            SELECT *
            FROM alerts
            WHERE status != ?
            """,
            (AlertStatus.CLOSED.value,),
        )

        return [
            AlertMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]

    def list_by_status(
        self,
        status: AlertStatus,
    ) -> list[Alert]:
        rows = self._fetch_by_column(
            table=self.TABLE,
            column="status",
            value=status.value,
        )

        return [
            AlertMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]

    def list_by_severity(
        self,
        severity: Severity,
    ) -> list[Alert]:
        rows = self._fetch_by_column(
            table=self.TABLE,
            column="severity",
            value=severity.value,
        )

        return [
            AlertMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]

    def delete(
        self,
        id: UUID,
    ) -> None:
        self._delete(
            table=self.TABLE,
            id_column="id",
            id_value=str(id),
        )