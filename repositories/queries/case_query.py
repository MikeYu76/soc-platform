from __future__ import annotations

from common.case_priority import CasePriority
from common.case_status import CaseStatus
from repositories.queries.base import Query


class CaseQuery(Query):
    """
    Query criteria for searching cases.
    """

    status: CaseStatus | None = None

    priority: CasePriority | None = None

    assigned_to: str | None = None
