from datetime import UTC, datetime
from ipaddress import ip_address

from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType
from enrichment.ip_classification import IPClassificationEnricher


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


def test_ip_classification_enricher_identifies_private_ip():
    detection = create_test_detection("192.168.1.50")
    enricher = IPClassificationEnricher()

    result = enricher.enrich(detection)

    assert result.data == {
        "ip_classification": {
            "source_ip": "192.168.1.50",
            "is_private": True,
            "is_loopback": False,
            "is_link_local": False,
            "is_global": False,
        }
    }


def test_ip_classification_enricher_identifies_global_ip():
    detection = create_test_detection("8.8.8.8")
    enricher = IPClassificationEnricher()

    result = enricher.enrich(detection)

    assert result.data == {
        "ip_classification": {
            "source_ip": "8.8.8.8",
            "is_private": False,
            "is_loopback": False,
            "is_link_local": False,
            "is_global": True,
        }
    }


def test_ip_classification_enricher_returns_empty_data_when_ip_is_missing():
    detection = create_test_detection(None)
    enricher = IPClassificationEnricher()

    result = enricher.enrich(detection)

    assert result.data == {}
