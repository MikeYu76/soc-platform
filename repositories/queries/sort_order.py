from __future__ import annotations

from enum import StrEnum


class SortOrder(StrEnum):
    """
    Sort direction for repository queries.
    """

    ASC = "asc"
    DESC = "desc"