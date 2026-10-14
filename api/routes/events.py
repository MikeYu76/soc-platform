from fastapi import APIRouter, Depends

from api.dependencies import (
    get_process_security_event_service,
)

from application.dto.process_security_event import (
    ProcessSecurityEventRequest,
    ProcessSecurityEventResponse,
)
from application.services.process_security_event import (
    ProcessSecurityEventService,
)

router = APIRouter(
    prefix="/events",
    tags=["Events"],
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

    Pipeline:

    Event
        ↓
    Detection
        ↓
    Enrichment
        ↓
    Correlation
        ↓
    Alert Creation
        ↓
    Alert Processing
        ↓
    Case Creation
        ↓
    Case Processing
        ↓
    Persistence
    """
    return service.execute(request)