from __future__ import annotations

from datetime import UTC, datetime

import pytest

from alert.factory import AlertFactory
from alert.models import Alert
from alert.processing.base import AlertProcessor
from alert.processing.engine import AlertProcessingEngine

from application.dto.process_security_event import (
    ProcessSecurityEventRequest,
)
from application.services.process_security_event import (
    ProcessSecurityEventService,
)

from case.factory import CaseFactory
from case.models import Case
from case.processing.base import CaseProcessor
from case.processing.engine import CaseProcessingEngine

from common.alert_status import AlertStatus
from common.case_status import CaseStatus
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
from enrichment.models import (
    EnrichedDetection,
    Enrichment,
)

from infrastructure.sqlite.connection import (
    SQLiteConnectionFactory,
)
from infrastructure.sqlite.sqlite_unit_of_work import (
    SQLiteUnitOfWork,
)


class MatchRule(DetectionRule):
    def match(self, event: Event) -> Detection | None:
        return Detection(
            rule_id="TEST-001",
            title="Test Detection",
            severity=Severity.LOW,
            event=event,
        )


class TestEnricher(Enricher):
    def enrich(
        self,
        detection: Detection,
    ) -> Enrichment:
        return Enrichment(
            data={
                "test": {
                    "value": "enriched",
                }
            }
        )


class TestCorrelationRule(CorrelationRule):
    def correlate(
        self,
        detections: list[EnrichedDetection],
    ) -> list[CorrelationResult]:
        return [
            CorrelationResult(
                correlation_id="corr-001",
                rule_id="CORR-001",
                title="Test Correlation",
                severity=Severity.HIGH,
                matched_at=datetime.now(UTC),
                detections=detections,
                metadata={},
            )
        ]


class TestAlertProcessor(AlertProcessor):
    def process(
        self,
        alerts: list[Alert],
    ) -> list[Alert]:
        for alert in alerts:
            alert.metadata["processed"] = True

        return alerts


class TestCaseProcessor(CaseProcessor):
    def process(
        self,
        cases: list[Case],
    ) -> list[Case]:
        for case in cases:
            case.metadata["processed"] = True

        return cases


@pytest.fixture
def connection_factory(
    tmp_path,
) -> SQLiteConnectionFactory:
    return SQLiteConnectionFactory(
        str(tmp_path / "test.db"),
    )


def make_event() -> Event:
    return Event(
        timestamp=datetime.now(UTC),
        log_source="Windows",
        event_type=EventType.AUTHENTICATION_FAILED,
        message="Failed login",
        raw_message="Event 4625",
    )


def test_process_security_event(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    service = ProcessSecurityEventService(
        unit_of_work_factory=lambda: SQLiteUnitOfWork(
            connection_factory,
        ),
        detection_engine=DetectionEngine(
            [MatchRule()],
        ),
        enrichment_engine=EnrichmentEngine(
            [TestEnricher()],
        ),
        correlation_engine=CorrelationEngine(
            [TestCorrelationRule()],
        ),
        alert_factory=AlertFactory(),
        alert_processing_engine=AlertProcessingEngine(
            [TestAlertProcessor()],
        ),
        case_factory=CaseFactory(),
        case_processing_engine=CaseProcessingEngine(
            [TestCaseProcessor()],
        ),
    )

    event = make_event()

    response = service.execute(
        ProcessSecurityEventRequest(
            event=event,
        )
    )

    with SQLiteUnitOfWork(connection_factory) as uow:
        loaded_event = uow.events.get(event.event_id)

        loaded_detections = uow.detections.list_by_rule(
            "TEST-001",
        )

        loaded_alerts = uow.alerts.list_by_status(
            AlertStatus.NEW,
        )

        loaded_cases = uow.cases.list_by_status(
            CaseStatus.NEW,
        )

    assert loaded_event is not None
    assert loaded_event.event_id == event.event_id

    assert len(loaded_detections) == 1
    persisted_detection = loaded_detections[0]

    assert len(loaded_alerts) == 1
    persisted_alert = loaded_alerts[0]

    assert len(loaded_cases) == 1
    persisted_case = loaded_cases[0]

    # Event
    assert response.event == event

    # Detection
    assert len(response.detections) == 1

    detection = response.detections[0]

    assert detection.detection_id == persisted_detection.detection_id
    assert detection.rule_id == "TEST-001"
    assert detection.title == "Test Detection"
    assert detection.severity == Severity.LOW
    assert detection.event == event

    # Enrichment
    assert len(response.enriched_detections) == 1

    enriched = response.enriched_detections[0]

    assert enriched.detection == detection

    assert enriched.enrichment.data == {
        "test": {
            "value": "enriched",
        }
    }

    # Correlation
    assert len(response.correlations) == 1

    correlation = response.correlations[0]

    assert correlation.correlation_id == "corr-001"
    assert correlation.rule_id == "CORR-001"
    assert correlation.title == "Test Correlation"
    assert correlation.severity == Severity.HIGH
    assert correlation.detections == response.enriched_detections

    # Alert
    assert len(response.alerts) == 1

    alert = response.alerts[0]

    assert alert.alert_id == persisted_alert.alert_id
    assert alert.title == "Test Correlation"
    assert alert.severity == Severity.HIGH
    assert alert.status == AlertStatus.NEW
    assert alert.source == correlation
    assert alert.metadata == {
        "processed": True,
    }

    # Case
    assert len(response.cases) == 1

    case = response.cases[0]

    assert case.case_id == persisted_case.case_id
    assert case.title == "Test Correlation"
    assert case.status == CaseStatus.NEW
    assert case.alert == alert
    assert case.metadata == {
        "processed": True,
    }

    assert len(case.timeline) == 1
    assert case.timeline[0].description == "Case created."