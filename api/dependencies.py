from application.composition.dependencies import (
    acknowledge_alert_service,
    add_case_comment_service,
    add_case_evidence_service,
    assign_case_service,
    close_alert_service,
    close_case_service,
    get_alert_service,
    get_case_service,
    get_case_timeline_service,
    get_event_service,
    list_alerts_service,
    list_cases_service,
    list_events_service,
    process_security_event_service,
    resolve_case_service,
    start_alert_investigation_service,
    start_case_investigation_service,
)
from application.services.acknowledge_alert import AcknowledgeAlertService
from application.services.add_case_comment import AddCaseCommentService
from application.services.add_case_evidence import AddCaseEvidenceService
from application.services.assign_case import AssignCaseService
from application.services.close_alert import CloseAlertService
from application.services.close_case import CloseCaseService
from application.services.get_alert import GetAlertService
from application.services.get_case import GetCaseService
from application.services.get_case_timeline import GetCaseTimelineService
from application.services.get_event import GetEventService
from application.services.list_alerts import ListAlertsService
from application.services.list_cases import ListCasesService
from application.services.list_events import ListEventsService
from application.services.process_security_event import (
    ProcessSecurityEventService,
)
from application.services.resolve_case import ResolveCaseService
from application.services.start_alert_investigation import (
    StartAlertInvestigationService,
)
from application.services.start_case_investigation import (
    StartCaseInvestigationService,
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


def get_start_alert_investigation_service() -> StartAlertInvestigationService:
    return start_alert_investigation_service


def get_close_alert_service() -> CloseAlertService:
    return close_alert_service


def get_get_case_service() -> GetCaseService:
    return get_case_service


def get_get_case_timeline_service() -> GetCaseTimelineService:
    return get_case_timeline_service


def get_list_cases_service() -> ListCasesService:
    return list_cases_service


def get_assign_case_service() -> AssignCaseService:
    return assign_case_service


def get_start_case_investigation_service() -> StartCaseInvestigationService:
    return start_case_investigation_service


def get_resolve_case_service() -> ResolveCaseService:
    return resolve_case_service


def get_close_case_service() -> CloseCaseService:
    return close_case_service


def get_add_case_comment_service() -> AddCaseCommentService:
    return add_case_comment_service


def get_add_case_evidence_service() -> AddCaseEvidenceService:
    return add_case_evidence_service
