from __future__ import annotations

from fastapi import APIRouter, Depends

from api.dependencies import (
    get_get_case_service,
    get_list_cases_service,
)

from application.dto.base import Request
from application.dto.case import (
    GetCaseResponse,
    ListCasesResponse,
)
from application.dto.identifier import IdentifierRequest

from application.services.get_case import GetCaseService
from application.services.list_cases import ListCasesService

router = APIRouter(
    prefix="/cases",
    tags=["Cases"],
)


@router.get(
    "",
    response_model=ListCasesResponse,
    summary="List active cases",
)
def list_cases(
    service: ListCasesService = Depends(
        get_list_cases_service,
    ),
) -> ListCasesResponse:
    return service.execute(
        Request(),
    )


@router.get(
    "/{id}",
    response_model=GetCaseResponse,
    summary="Retrieve a case",
)
def get_case(
    id: str,
    service: GetCaseService = Depends(
        get_get_case_service,
    ),
) -> GetCaseResponse:
    return service.execute(
        IdentifierRequest(
            id=id,
        )
    )