from __future__ import annotations

from common.case_priority import CasePriority
from common.case_status import CaseStatus
from repositories.queries.base import Query
from repositories.queries.case_sort import CaseSort
from repositories.queries.sort_order import SortOrder


class CaseQuery(Query):
    """
    Query criteria for searching cases.
    """

    status: CaseStatus | None = None

    priority: CasePriority | None = None

    assigned_to: str | None = None

    sort_by: CaseSort = CaseSort.CREATED_AT

    sort_order: SortOrder = SortOrder.DESC

    limit: int = 50

    offset: int = 0
