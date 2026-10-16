from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.dependencies import (
    get_assign_case_service,
    get_close_case_service,
    get_get_case_service,
    get_list_cases_service,
    get_resolve_case_service,
    get_start_case_investigation_service,
)

from application.dto.base import Request
from application.dto.case import (
    AssignCaseRequest,
    AssignCaseResponse,
    CloseCaseRequest,
    CloseCaseResponse,
    GetCaseResponse,
    ListCasesResponse,
    ResolveCaseRequest,
    ResolveCaseResponse,
    StartCaseInvestigationRequest,
    StartCaseInvestigationResponse,
)
from application.dto.identifier import IdentifierRequest

from application.services.assign_case import AssignCaseService
from application.services.close_case import CloseCaseService
from application.services.get_case import GetCaseService
from application.services.list_cases import ListCasesService
from application.services.resolve_case import ResolveCaseService
from application.services.start_case_investigation import (
    StartCaseInvestigationService,
)


class AssignCaseBody(BaseModel):
    team: str
    assigned_by: str
    reason: str


class StartCaseInvestigationBody(BaseModel):
    analyst: str


class ResolveCaseBody(BaseModel):
    resolution_type: str
    summary: str
    resolved_by: str


class CloseCaseBody(BaseModel):
    closed_by: str


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


@router.patch(
    "/{id}/assign",
    response_model=AssignCaseResponse,
    summary="Assign a case",
)
def assign_case(
    id: str,
    body: AssignCaseBody,
    service: AssignCaseService = Depends(
        get_assign_case_service,
    ),
) -> AssignCaseResponse:
    return service.execute(
        AssignCaseRequest(
            case_id=id,
            team=body.team,
            assigned_by=body.assigned_by,
            reason=body.reason,
        )
    )


@router.patch(
    "/{id}/start",
    response_model=StartCaseInvestigationResponse,
    summary="Start a case investigation",
)
def start_case_investigation(
    id: str,
    body: StartCaseInvestigationBody,
    service: StartCaseInvestigationService = Depends(
        get_start_case_investigation_service,
    ),
) -> StartCaseInvestigationResponse:
    return service.execute(
        StartCaseInvestigationRequest(
            case_id=id,
            analyst=body.analyst,
        )
    )


@router.patch(
    "/{id}/resolve",
    response_model=ResolveCaseResponse,
    summary="Resolve a case",
)
def resolve_case(
    id: str,
    body: ResolveCaseBody,
    service: ResolveCaseService = Depends(
        get_resolve_case_service,
    ),
) -> ResolveCaseResponse:
    return service.execute(
        ResolveCaseRequest(
            case_id=id,
            resolution_type=body.resolution_type,
            summary=body.summary,
            resolved_by=body.resolved_by,
        )
    )


@router.patch(
    "/{id}/close",
    response_model=CloseCaseResponse,
    summary="Close a case",
)
def close_case(
    id: str,
    body: CloseCaseBody,
    service: CloseCaseService = Depends(
        get_close_case_service,
    ),
) -> CloseCaseResponse:
    return service.execute(
        CloseCaseRequest(
            case_id=id,
            closed_by=body.closed_by,
        )
    )