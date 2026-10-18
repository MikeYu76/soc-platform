from __future__ import annotations

from pydantic import BaseModel, Field

from repositories.queries.sort_order import SortOrder


class Query(BaseModel):
    """
    Base query object shared by repository search operations.
    """

    limit: int = Field(
        default=50,
        ge=1,
    )

    offset: int = Field(
        default=0,
        ge=0,
    )

    sort_by: str | None = None

    sort_order: SortOrder = SortOrder.DESC
