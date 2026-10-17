from __future__ import annotations

from dataclasses import dataclass

from application.dto.base import Request, Response
from case.models import Case


@dataclass(slots=True)
class GetCaseResponse(Response):
    """
    Response containing a single case.
    """

    case: Case


@dataclass(slots=True)
class ListCasesResponse(Response):
    """
    Response containing active cases.
    """

    cases: list[Case]


@dataclass(slots=True)
class AssignCaseRequest(Request):
    """
    Request to assign a case.
    """

    case_id: str

    team: str

    assigned_by: str

    reason: str


@dataclass(slots=True)
class AssignCaseResponse(Response):
    """
    Response after assigning a case.
    """

    case: Case


@dataclass(slots=True)
class StartCaseInvestigationRequest(Request):
    """
    Request to start a case investigation.
    """

    case_id: str

    analyst: str


@dataclass(slots=True)
class StartCaseInvestigationResponse(Response):
    """
    Response after starting a case investigation.
    """

    case: Case


@dataclass(slots=True)
class ResolveCaseRequest(Request):
    """
    Request to resolve a case.
    """

    case_id: str

    resolution_type: str

    summary: str

    resolved_by: str


@dataclass(slots=True)
class ResolveCaseResponse(Response):
    """
    Response after resolving a case.
    """

    case: Case


@dataclass(slots=True)
class CloseCaseRequest(Request):
    """
    Request to close a case.
    """

    case_id: str

    closed_by: str


@dataclass(slots=True)
class CloseCaseResponse(Response):
    """
    Response after closing a case.
    """

    case: Case
