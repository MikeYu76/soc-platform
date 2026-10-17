from datetime import UTC, datetime
from uuid import uuid4

from alert.correlation_alert import CorrelationAlertRule
from alert.engine import AlertEngine
from alert.immediate_detection import ImmediateDetectionAlertRule
from alert.processing.engine import AlertProcessingEngine
from application.dto.process_security_event import ProcessSecurityEventRequest
from application.services.process_security_event import (
    ProcessSecurityEventService,
)
from case.factory import CaseFactory
from case.processing.engine import CaseProcessingEngine
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType
from correlation.base import CorrelationRule
from correlation.engine import CorrelationEngine
from correlation.models import CorrelationResult
from detection.base import DetectionRule
from detection.engine import DetectionEngine
from enrichment.base import Enricher
from enrichment.engine import EnrichmentEngine
from enrichment.models import EnrichedDetection, Enrichment
from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.sqlite_unit_of_work import SQLiteUnitOfWork


class MatchRule(DetectionRule):
    def match(
        self,
        event: Event,
    ) -> Detection | None:
        return Detection(
            rule_id="TEST-001",
            title="Test Detection",
            severity=Severity.HIGH,
            event=event,
        )


class TestEnricher(Enricher):
    def enrich(
        self,
        detection: Detection,
    ) -> Enrichment:
        return Enrichment(
            data={
                "test": True,
            }
        )


class TestCorrelationRule(CorrelationRule):
    def correlate(
        self,
        detections: list[EnrichedDetection],
    ) -> list[CorrelationResult]:
        return [
            CorrelationResult(
                correlation_id=str(uuid4()),
                rule_id="TEST-CORRELATION-001",
                title="Test Correlation",
                severity=Severity.HIGH,
                matched_at=datetime.now(UTC),
                detections=detections,
            )
        ]


class TestAlertProcessor:
    def process(
        self,
        alerts,
    ):
        return alerts


class TestCaseProcessor:
    def process(
        self,
        cases,
    ):
        return cases


def make_event() -> Event:
    return Event(
        timestamp=datetime.now(UTC),
        log_source="windows",
        event_type=EventType.AUTHENTICATION_FAILED,
        message="Failed login",
        raw_message="Raw failed login",
        hostname="dc01",
        username="administrator",
    )


def test_process_security_event(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    service = ProcessSecurityEventService(
        unit_of_work_factory=lambda: SQLiteUnitOfWork(
            connection_factory,
        ),
        detection_engine=DetectionEngine(
            [
                MatchRule(),
            ]
        ),
        enrichment_engine=EnrichmentEngine(
            [
                TestEnricher(),
            ]
        ),
        correlation_engine=CorrelationEngine(
            [
                TestCorrelationRule(),
            ]
        ),
        alert_engine=AlertEngine(
            [
                ImmediateDetectionAlertRule(),
                CorrelationAlertRule(),
            ]
        ),
        alert_processing_engine=AlertProcessingEngine(
            [
                TestAlertProcessor(),
            ]
        ),
        case_factory=CaseFactory(),
        case_processing_engine=CaseProcessingEngine(
            [
                TestCaseProcessor(),
            ]
        ),
    )

    request = ProcessSecurityEventRequest(
        event=make_event(),
    )

    response = service.execute(
        request,
    )

    assert response.event == request.event

    assert len(response.detections) == 1
    assert response.detections[0].title == "Test Detection"

    assert len(response.enriched_detections) == 1

    assert len(response.correlations) == 1
    assert response.correlations[0].title == "Test Correlation"

    assert len(response.alerts) == 2
    assert len(response.cases) == 2

    with SQLiteUnitOfWork(connection_factory) as uow:
        assert uow.events.get(request.event.id) is not None
        assert len(uow.detections.list_all()) == 1
        assert len(uow.alerts.list_active()) == 2
        assert len(uow.cases.list_active()) == 2
