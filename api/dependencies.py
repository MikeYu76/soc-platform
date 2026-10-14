from application.composition.dependencies import (
    process_security_event_service,
)
from application.services.process_security_event import (
    ProcessSecurityEventService,
)


def get_process_security_event_service() -> ProcessSecurityEventService:
    """
    Returns the application's ProcessSecurityEventService.

    FastAPI uses this function for dependency injection.
    """
    return process_security_event_service