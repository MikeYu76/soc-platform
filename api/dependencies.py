from application.composition.dependencies import (
    acknowledge_alert_service,
    get_alert_service,
    get_case_service,
    get_event_service,
    list_alerts_service,
    list_cases_service,
    list_events_service,
    process_security_event_service,
)

from application.services.acknowledge_alert import (
    AcknowledgeAlertService,
)
from application.services.get_alert import GetAlertService
from application.services.get_case import GetCaseService
from application.services.get_event import GetEventService
from application.services.list_alerts import ListAlertsService
from application.services.list_cases import ListCasesService
from application.services.list_events import ListEventsService
from application.services.process_security_event import (
    ProcessSecurityEventService,
)


def get_process_security_event_service() -> ProcessSecurityEventService:
    return process_security_event_service


def get_get_event_service() -> GetEventService:
    return get_event_service


def get_list_events_service() -> ListEventsService:
    return list_events_service


def get_get_alert_service() -> GetAlertService:
    return get_alert_service


def get_list_alerts_service() -> ListAlertsService:
    return list_alerts_service


def get_acknowledge_alert_service() -> AcknowledgeAlertService:
    return acknowledge_alert_service


def get_get_case_service() -> GetCaseService:
    return get_case_service


def get_list_cases_service() -> ListCasesService:
    return list_cases_service