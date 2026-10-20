from datetime import UTC, datetime
from ipaddress import ip_address

from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType
from enrichment.ip_context import IPContextEnricher


def create_test_detection(source_ip: str | None) -> Detection:
    """Create a detection with a configurable source IP."""

    return Detection(
        rule_id="AUTH-001",
        title="Windows Failed Login",
        severity=Severity.MEDIUM,
        event=Event(
            timestamp=datetime(2026, 10, 8, 12, 0, tzinfo=UTC),
            log_source="windows",
            event_type=EventType.AUTHENTICATION_FAILED,
            message="Failed login attempt",
            raw_message="Sample Windows failed login event",
            source_ip=ip_address(source_ip) if source_ip is not None else None,
        ),
    )


def test_ip_context_enricher_returns_context_for_known_ip():
    ip_context = {
        "192.168.1.50": {
            "label": "known_test_host",
            "risk": "low",
        }
    }

    enricher = IPContextEnricher(ip_context)
    detection = create_test_detection("192.168.1.50")

    result = enricher.enrich(detection)

    assert result.data == {
        "ip_context": {
            "source_ip": "192.168.1.50",
            "label": "known_test_host",
            "risk": "low",
        }
    }


def test_ip_context_enricher_returns_empty_data_for_unknown_ip():
    ip_context = {
        "192.168.1.50": {
            "label": "known_test_host",
            "risk": "low",
        }
    }

    enricher = IPContextEnricher(ip_context)
    detection = create_test_detection("203.0.113.25")

    result = enricher.enrich(detection)

    assert result.data == {}


def test_ip_context_enricher_returns_empty_data_when_source_ip_is_missing():
    ip_context = {
        "192.168.1.50": {
            "label": "known_test_host",
            "risk": "low",
        }
    }

    enricher = IPContextEnricher(ip_context)
    detection = create_test_detection(None)

    result = enricher.enrich(detection)

    assert result.data == {}
