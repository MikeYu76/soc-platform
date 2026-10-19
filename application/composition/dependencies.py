from __future__ import annotations

from alert.correlation_alert import CorrelationAlertRule
from alert.engine import AlertEngine
from alert.immediate_detection import ImmediateDetectionAlertRule
from alert.processing import (
    AlertGroupingProcessor,
    AlertProcessingEngine,
    AlertRoutingProcessor,
    DeduplicationProcessor,
)
from application.composition.settings import (
    Settings,
    get_settings,
)
from application.services.acknowledge_alert import (
    AcknowledgeAlertService,
)
from application.services.add_case_comment import AddCaseCommentService
from application.services.add_case_evidence import AddCaseEvidenceService
from application.services.assign_case import (
    AssignCaseService,
)
from application.services.close_alert import (
    CloseAlertService,
)
from application.services.close_case import (
    CloseCaseService,
)
from application.services.change_case_priority import ChangeCasePriorityService
from application.services.get_alert import GetAlertService
from application.services.get_case import GetCaseService
from application.services.get_case_timeline import GetCaseTimelineService
from application.services.get_event import GetEventService
from application.services.list_alerts import (
    ListAlertsService,
)
from application.services.list_cases import (
    ListCasesService,
)
from application.services.list_events import (
    ListEventsService,
)
from application.services.process_security_event import (
    ProcessSecurityEventService,
)
from application.services.resolve_case import (
    ResolveCaseService,
)
from application.services.start_alert_investigation import (
    StartAlertInvestigationService,
)
from application.services.start_case_investigation import (
    StartCaseInvestigationService,
)
from case.factory import CaseFactory
from case.processing import (
    CaseAssignmentProcessor,
    CaseEscalationProcessor,
    CaseProcessingEngine,
    CaseSLABreachProcessor,
    CaseSLAProcessor,
)
from correlation.engine import CorrelationEngine
from correlation.rules import (
    FailedLoginBurstRule,
    ImpossibleTravelRule,
    LateralMovementRule,
    PrivilegeEscalationRule,
)
from detection.engine import DetectionEngine
from detection.rules.failed_login import FailedLoginRule
from enrichment.engine import EnrichmentEngine
from enrichment.ip_classification import (
    IPClassificationEnricher,
)
from enrichment.ip_context import (
    IPContextEnricher,
)
from infrastructure.sqlite.connection import (
    SQLiteConnectionFactory,
)
from infrastructure.sqlite.sqlite_unit_of_work import (
    SQLiteUnitOfWork,
)

settings: Settings = get_settings()

connection_factory = SQLiteConnectionFactory(
    settings.database_path,
)


def unit_of_work_factory() -> SQLiteUnitOfWork:
    return SQLiteUnitOfWork(
        connection_factory,
    )


ip_context: dict[str, dict[str, str]] = {
    "8.8.8.8": {
        "country": "United States",
        "organization": "Google",
    },
    "1.1.1.1": {
        "country": "Australia",
        "organization": "Cloudflare",
    },
}


detection_engine = DetectionEngine(
    [
        FailedLoginRule(),
    ]
)


enrichment_engine = EnrichmentEngine(
    [
        IPContextEnricher(
            ip_context=ip_context,
        ),
        IPClassificationEnricher(),
    ]
)


correlation_engine = CorrelationEngine(
    [
        FailedLoginBurstRule(),
        ImpossibleTravelRule(),
        LateralMovementRule(),
        PrivilegeEscalationRule(),
    ]
)


alert_engine = AlertEngine(
    [
        ImmediateDetectionAlertRule(),
        CorrelationAlertRule(),
    ]
)


alert_processing_engine = AlertProcessingEngine(
    [
        DeduplicationProcessor(),
        AlertGroupingProcessor(),
        AlertRoutingProcessor(),
    ]
)


case_factory = CaseFactory()


case_processing_engine = CaseProcessingEngine(
    [
        CaseAssignmentProcessor(),
        CaseSLAProcessor(),
        CaseSLABreachProcessor(),
        CaseEscalationProcessor(),
    ]
)


process_security_event_service = ProcessSecurityEventService(
    unit_of_work_factory=unit_of_work_factory,
    detection_engine=detection_engine,
    enrichment_engine=enrichment_engine,
    correlation_engine=correlation_engine,
    alert_engine=alert_engine,
    alert_processing_engine=alert_processing_engine,
    case_factory=case_factory,
    case_processing_engine=case_processing_engine,
)


get_event_service = GetEventService(
    unit_of_work_factory=unit_of_work_factory,
)


list_events_service = ListEventsService(
    unit_of_work_factory=unit_of_work_factory,
)


get_alert_service = GetAlertService(
    unit_of_work_factory=unit_of_work_factory,
)


list_alerts_service = ListAlertsService(
    unit_of_work_factory=unit_of_work_factory,
)


acknowledge_alert_service = AcknowledgeAlertService(
    unit_of_work_factory=unit_of_work_factory,
)


start_alert_investigation_service = StartAlertInvestigationService(
    unit_of_work_factory=unit_of_work_factory,
)


close_alert_service = CloseAlertService(
    unit_of_work_factory=unit_of_work_factory,
)


get_case_service = GetCaseService(
    unit_of_work_factory=unit_of_work_factory,
)


get_case_timeline_service = GetCaseTimelineService(
    unit_of_work_factory=unit_of_work_factory,
)


list_cases_service = ListCasesService(
    unit_of_work_factory=unit_of_work_factory,
)


assign_case_service = AssignCaseService(
    unit_of_work_factory=unit_of_work_factory,
)


start_case_investigation_service = StartCaseInvestigationService(
    unit_of_work_factory=unit_of_work_factory,
)


resolve_case_service = ResolveCaseService(
    unit_of_work_factory=unit_of_work_factory,
)


close_case_service = CloseCaseService(
    unit_of_work_factory=unit_of_work_factory,
)


add_case_comment_service = AddCaseCommentService(
    unit_of_work_factory=unit_of_work_factory,
)


add_case_evidence_service = AddCaseEvidenceService(
    unit_of_work_factory=unit_of_work_factory,
)


change_case_priority_service = ChangeCasePriorityService(
    unit_of_work_factory=unit_of_work_factory,
)
