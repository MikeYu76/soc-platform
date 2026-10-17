from datetime import UTC, datetime

from alert.correlation_alert import CorrelationAlertRule
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType
from correlation.models import CorrelationResult
from enrichment.models import EnrichedDetection, Enrichment


def build_detection() -> Detection:
    event = Event(
        timestamp=datetime.now(UTC),
        log_source="windows",
        event_type=EventType.AUTHENTICATION_SUCCESS,
        message="User logged in",
        raw_message="raw",
    )

    return Detection(
        rule_id="DET-001",
        title="Successful Login",
        severity=Severity.MEDIUM,
        event=event,
    )


def build_correlation() -> CorrelationResult:
    detection = build_detection()

    enriched = EnrichedDetection(
        detection=detection,
        enrichment=Enrichment(data={}),
    )

    return CorrelationResult(
        correlation_id="CORR-001",
        rule_id="CORR-RULE-001",
        title="Impossible Travel",
        severity=Severity.HIGH,
        matched_at=datetime.now(UTC),
        detections=[enriched],
    )


def test_returns_empty_list_when_no_correlations():
    rule = CorrelationAlertRule()

    alerts = rule.generate([], [])

    assert alerts == []


def test_generates_alert_for_correlation():
    correlation = build_correlation()

    rule = CorrelationAlertRule()

    alerts = rule.generate([], [correlation])

    assert len(alerts) == 1


def test_alert_copies_title():
    correlation = build_correlation()

    rule = CorrelationAlertRule()

    alert = rule.generate([], [correlation])[0]

    assert alert.title == correlation.title


def test_alert_copies_severity():
    correlation = build_correlation()

    rule = CorrelationAlertRule()

    alert = rule.generate([], [correlation])[0]

    assert alert.severity == correlation.severity


def test_alert_source_is_correlation():
    correlation = build_correlation()

    rule = CorrelationAlertRule()

    alert = rule.generate([], [correlation])[0]

    assert alert.source is correlation


def test_multiple_correlations_generate_multiple_alerts():
    rule = CorrelationAlertRule()

    correlations = [
        build_correlation(),
        build_correlation(),
    ]

    alerts = rule.generate([], correlations)

    assert len(alerts) == 2
