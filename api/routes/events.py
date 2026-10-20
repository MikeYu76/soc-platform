from fastapi import APIRouter, Depends, Query
from pydantic import IPvAnyAddress

from api.dependencies import (
    get_get_event_service,
    get_list_events_service,
    get_process_security_event_service,
)
from api.security import get_current_user, require_roles
from application.dto.get_event import GetEventResponse
from application.dto.identifier import IdentifierRequest
from application.dto.list_events import ListEventsRequest, ListEventsResponse
from application.dto.process_security_event import (
    ProcessSecurityEventRequest,
    ProcessSecurityEventResponse,
)
from application.services.get_event import GetEventService
from application.services.list_events import ListEventsService
from application.services.process_security_event import (
    ProcessSecurityEventService,
)
from common.event_types import EventType
from common.user_role import UserRole
from identity.user import User
from repositories.queries.event_query import EventQuery
from repositories.queries.event_sort import EventSort
from repositories.queries.sort_order import SortOrder

router = APIRouter(
    prefix="/events",
    tags=["Events"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "",
    response_model=ListEventsResponse,
    summary="List security events",
)
def list_events(
    event_type: EventType | None = Query(
        default=None,
        description="Filter by event type.",
    ),
    hostname: str | None = Query(
        default=None,
        description="Filter by hostname.",
    ),
    username: str | None = Query(
        default=None,
        description="Filter by username.",
    ),
    log_source: str | None = Query(
        default=None,
        description="Filter by log source.",
    ),
    source_ip: IPvAnyAddress | None = Query(
        default=None,
        description="Filter by source IP address.",
    ),
    destination_ip: IPvAnyAddress | None = Query(
        default=None,
        description="Filter by destination IP address.",
    ),
    sort_by: EventSort = Query(
        default=EventSort.TIMESTAMP,
        description="Field to sort by.",
    ),
    order: SortOrder = Query(
        default=SortOrder.DESC,
        description="Sort order.",
    ),
    limit: int = Query(
        default=50,
        ge=1,
        description="Maximum number of events to return.",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of events to skip.",
    ),
    service: ListEventsService = Depends(
        get_list_events_service,
    ),
) -> ListEventsResponse:
    """
    Retrieve persisted security events.
    """
    return service.execute(
        ListEventsRequest(
            query=EventQuery(
                event_type=event_type,
                hostname=hostname,
                username=username,
                log_source=log_source,
                source_ip=source_ip,
                destination_ip=destination_ip,
                sort_by=sort_by,
                sort_order=order,
                limit=limit,
                offset=offset,
            ),
        ),
    )


@router.get(
    "/{id}",
    response_model=GetEventResponse,
    summary="Retrieve a security event",
)
def get_event(
    id: str,
    service: GetEventService = Depends(
        get_get_event_service,
    ),
) -> GetEventResponse:
    """
    Retrieve a security event by its internal identifier.
    """
    return service.execute(
        IdentifierRequest(
            id=id,
        )
    )


@router.post(
    "",
    response_model=ProcessSecurityEventResponse,
    summary="Process a security event",
)
def process_security_event(
    request: ProcessSecurityEventRequest,
    service: ProcessSecurityEventService = Depends(
        get_process_security_event_service,
    ),
    _user: User = Depends(
        require_roles(
            UserRole.INCIDENT_RESPONDER,
            UserRole.SOC_MANAGER,
            UserRole.ADMINISTRATOR,
        )
    ),
) -> ProcessSecurityEventResponse:
    """
    Execute the complete SOC processing pipeline for a normalized
    security event.
    """
    return service.execute(request)
