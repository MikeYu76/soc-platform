from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field

from api.dependencies import (
    get_add_case_comment_service,
    get_add_case_evidence_service,
    get_assign_case_service,
    get_close_case_service,
    get_change_case_priority_service,
    get_get_case_service,
    get_get_case_timeline_service,
    get_list_cases_service,
    get_resolve_case_service,
    get_start_case_investigation_service,
)
from api.security import get_current_user, require_roles
from application.dto.case import (
    AddCaseCommentRequest,
    AddCaseCommentResponse,
    AddCaseEvidenceRequest,
    AddCaseEvidenceResponse,
    AssignCaseRequest,
    AssignCaseResponse,
    CloseCaseRequest,
    CloseCaseResponse,
    ChangeCasePriorityRequest,
    ChangeCasePriorityResponse,
    GetCaseResponse,
    GetCaseTimelineResponse,
    ListCasesRequest,
    ListCasesResponse,
    ResolveCaseRequest,
    ResolveCaseResponse,
    StartCaseInvestigationRequest,
    StartCaseInvestigationResponse,
)
from application.dto.identifier import IdentifierRequest
from application.services.add_case_comment import AddCaseCommentService
from application.services.add_case_evidence import AddCaseEvidenceService
from application.services.assign_case import AssignCaseService
from application.services.close_case import CloseCaseService
from application.services.change_case_priority import ChangeCasePriorityService
from application.services.get_case import GetCaseService
from application.services.get_case_timeline import GetCaseTimelineService
from application.services.list_cases import ListCasesService
from application.services.resolve_case import ResolveCaseService
from application.services.start_case_investigation import (
    StartCaseInvestigationService,
)
from common.case_priority import CasePriority
from common.case_status import CaseStatus
from common.user_role import UserRole
from identity.user import User
from repositories.queries.case_query import CaseQuery


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


class AddCaseCommentBody(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    author: str = Field(min_length=1)
    message: str = Field(min_length=1)


class AddCaseEvidenceBody(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    source: str = Field(min_length=1)


class ChangeCasePriorityBody(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    priority: CasePriority
    changed_by: str = Field(min_length=1)


router = APIRouter(
    prefix="/cases",
    tags=["Cases"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "",
    response_model=ListCasesResponse,
    summary="List active cases",
)
def list_cases(
    status: CaseStatus | None = None,
    priority: CasePriority | None = None,
    assigned_to: str | None = None,
    limit: int = 50,
    offset: int = 0,
    service: ListCasesService = Depends(
        get_list_cases_service,
    ),
) -> ListCasesResponse:
    return service.execute(
        ListCasesRequest(
            query=CaseQuery(
                status=status,
                priority=priority,
                assigned_to=assigned_to,
                limit=limit,
                offset=offset,
            ),
        )
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


@router.get(
    "/{id}/timeline",
    response_model=GetCaseTimelineResponse,
    summary="Retrieve a case timeline",
)
def get_case_timeline(
    id: str,
    service: GetCaseTimelineService = Depends(
        get_get_case_timeline_service,
    ),
) -> GetCaseTimelineResponse:
    return service.execute(IdentifierRequest(id=id))


@router.post(
    "/{id}/comments",
    response_model=AddCaseCommentResponse,
    summary="Add a comment to a case",
    status_code=201,
)
def add_case_comment(
    id: str,
    body: AddCaseCommentBody,
    service: AddCaseCommentService = Depends(
        get_add_case_comment_service,
    ),
    _user: User = Depends(
        require_roles(
            UserRole.ANALYST,
            UserRole.SENIOR_ANALYST,
            UserRole.INCIDENT_RESPONDER,
            UserRole.SOC_MANAGER,
            UserRole.ADMINISTRATOR,
        )
    ),
) -> AddCaseCommentResponse:
    return service.execute(
        AddCaseCommentRequest(
            case_id=id,
            author=body.author,
            message=body.message,
        )
    )


@router.post(
    "/{id}/evidence",
    response_model=AddCaseEvidenceResponse,
    summary="Add evidence to a case",
    status_code=201,
)
def add_case_evidence(
    id: str,
    body: AddCaseEvidenceBody,
    service: AddCaseEvidenceService = Depends(
        get_add_case_evidence_service,
    ),
    _user: User = Depends(
        require_roles(
            UserRole.ANALYST,
            UserRole.SENIOR_ANALYST,
            UserRole.INCIDENT_RESPONDER,
            UserRole.SOC_MANAGER,
            UserRole.ADMINISTRATOR,
        )
    ),
) -> AddCaseEvidenceResponse:
    return service.execute(
        AddCaseEvidenceRequest(
            case_id=id,
            name=body.name,
            description=body.description,
            source=body.source,
        )
    )


@router.patch(
    "/{id}/priority",
    response_model=ChangeCasePriorityResponse,
    summary="Change a case priority",
)
def change_case_priority(
    id: str,
    body: ChangeCasePriorityBody,
    service: ChangeCasePriorityService = Depends(
        get_change_case_priority_service,
    ),
    _user: User = Depends(
        require_roles(
            UserRole.SENIOR_ANALYST,
            UserRole.INCIDENT_RESPONDER,
            UserRole.SOC_MANAGER,
            UserRole.ADMINISTRATOR,
        )
    ),
) -> ChangeCasePriorityResponse:
    return service.execute(
        ChangeCasePriorityRequest(
            case_id=id,
            priority=body.priority.value,
            changed_by=body.changed_by,
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
    _user: User = Depends(
        require_roles(
            UserRole.SENIOR_ANALYST,
            UserRole.INCIDENT_RESPONDER,
            UserRole.SOC_MANAGER,
            UserRole.ADMINISTRATOR,
        )
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
    _user: User = Depends(
        require_roles(
            UserRole.ANALYST,
            UserRole.SENIOR_ANALYST,
            UserRole.INCIDENT_RESPONDER,
            UserRole.SOC_MANAGER,
            UserRole.ADMINISTRATOR,
        )
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
    _user: User = Depends(
        require_roles(
            UserRole.SENIOR_ANALYST,
            UserRole.INCIDENT_RESPONDER,
            UserRole.SOC_MANAGER,
            UserRole.ADMINISTRATOR,
        )
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
    _user: User = Depends(
        require_roles(
            UserRole.SENIOR_ANALYST,
            UserRole.INCIDENT_RESPONDER,
            UserRole.SOC_MANAGER,
            UserRole.ADMINISTRATOR,
        )
    ),
) -> CloseCaseResponse:
    return service.execute(
        CloseCaseRequest(
            case_id=id,
            closed_by=body.closed_by,
        )
    )
