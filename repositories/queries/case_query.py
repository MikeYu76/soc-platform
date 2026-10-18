from __future__ import annotations

from dataclasses import dataclass

from common.case_priority import CasePriority
from common.case_status import CaseStatus


@dataclass(slots=True)
class CaseQuery:
    """
    Query criteria for searching cases.
    """

    status: CaseStatus | None = None

    priority: CasePriority | None = None

    assigned_to: str | None = None
