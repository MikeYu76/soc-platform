from fastapi import APIRouter, Depends

from api.dependencies import (
    get_get_event_service,
    get_list_events_service,
    get_process_security_event_service,
)

from application.dto.identifier import IdentifierRequest
from application.dto.list_events import (
    ListEventsRequest,
    ListEventsResponse,
)
from application.dto.process_security_event import (
    ProcessSecurityEventRequest,
    ProcessSecurityEventResponse,
)
from application.dto.get_event import GetEventResponse

from application.services.get_event import GetEventService
from application.services.list_events import ListEventsService
from application.services.process_security_event import (
    ProcessSecurityEventService,
)

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.get(
    "",
    response_model=ListEventsResponse,
    summary="List security events",
)
def list_events(
    service: ListEventsService = Depends(
        get_list_events_service,
    ),
) -> ListEventsResponse:
    """
    Retrieve all persisted security events.
    """
    return service.execute(
        ListEventsRequest(),
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
) -> ProcessSecurityEventResponse:
    """
    Execute the complete SOC processing pipeline for a normalized
    security event.
    """
    return service.execute(request)