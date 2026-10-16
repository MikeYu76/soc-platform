from __future__ import annotations

from uuid import UUID

from case.models import Case

from common.case_priority import CasePriority
from common.case_status import CaseStatus

from infrastructure.sqlite.base_repository import SQLiteRepository
from infrastructure.sqlite.mappers.case_mapper import CaseMapper

from repositories.case_repository import CaseRepository


class SQLiteCaseRepository(
    SQLiteRepository,
    CaseRepository,
):
    """
    SQLite implementation of CaseRepository.
    """

    TABLE = "cases"

    def save(
        self,
        case: Case,
    ) -> None:
        self._upsert(
            table=self.TABLE,
            values=CaseMapper.to_record(case),
        )

    def update(
        self,
        case: Case,
    ) -> None:
        self._upsert(
            table=self.TABLE,
            values=CaseMapper.to_record(case),
        )

    def get(
        self,
        id: UUID,
    ) -> Case | None:
        row = self._fetch_one(
            """
            SELECT *
            FROM cases
            WHERE id = ?
            """,
            (str(id),),
        )

        if row is None:
            return None

        return CaseMapper.from_record(
            self._row_to_dict(row),
        )

    def list_active(
        self,
    ) -> list[Case]:
        rows = self._fetch_all(
            """
            SELECT *
            FROM cases
            WHERE status != ?
            """,
            (CaseStatus.CLOSED.value,),
        )

        return [
            CaseMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]

    def list_by_status(
        self,
        status: CaseStatus,
    ) -> list[Case]:
        rows = self._fetch_by_column(
            table=self.TABLE,
            column="status",
            value=status.value,
        )

        return [
            CaseMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]

    def list_by_priority(
        self,
        priority: CasePriority,
    ) -> list[Case]:
        rows = self._fetch_by_column(
            table=self.TABLE,
            column="priority",
            value=priority.value,
        )

        return [
            CaseMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]

    def list_assigned_to(
        self,
        team: str,
    ) -> list[Case]:
        rows = self._fetch_by_column(
            table=self.TABLE,
            column="assigned_to",
            value=team,
        )

        return [
            CaseMapper.from_record(
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