from __future__ import annotations

from dataclasses import dataclass, field

from application.dto.base import Request, Response
from case.domain.timeline import CaseTimelineEvent
from case.models import Case
from repositories.queries.case_query import CaseQuery


@dataclass(slots=True)
class GetCaseResponse(Response):
    """
    Response containing a single case.
    """

    case: Case


@dataclass(slots=True)
class GetCaseTimelineResponse(Response):
    """Response containing the timeline for a case."""

    timeline: list[CaseTimelineEvent]

    @classmethod
    def from_domain(
        cls,
        timeline: list[CaseTimelineEvent],
    ) -> GetCaseTimelineResponse:
        return cls(timeline=timeline)


@dataclass(slots=True)
class AddCaseCommentRequest(Request):
    """Request to add an analyst comment to a case."""

    case_id: str

    author: str

    message: str


@dataclass(slots=True)
class AddCaseCommentResponse(Response):
    """Response after adding a comment to a case."""

    case: Case


@dataclass(slots=True)
class AddCaseEvidenceRequest(Request):
    """Request to add evidence to a case."""

    case_id: str

    name: str

    description: str

    source: str


@dataclass(slots=True)
class AddCaseEvidenceResponse(Response):
    """Response after adding evidence to a case."""

    case: Case


@dataclass(slots=True)
class ListCasesRequest(Request):
    """
    Request to retrieve cases.
    """

    query: CaseQuery = field(
        default_factory=CaseQuery,
    )


@dataclass(slots=True)
class ListCasesResponse(Response):
    """
    Response containing cases.
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
