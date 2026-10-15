from __future__ import annotations

from pydantic import BaseModel

from case.models import Case


class GetCaseResponse(BaseModel):
    """
    Response returned when retrieving a single case.
    """

    case: Case


class ListCasesResponse(BaseModel):
    """
    Response returned when listing cases.
    """

    cases: list[Case]