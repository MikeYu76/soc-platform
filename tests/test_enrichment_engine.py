from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType

from enrichment.base import Enricher
from enrichment.engine import EnrichmentEngine
from enrichment.models import Enrichment


class GeoIPTestEnricher(Enricher):
    """Test enricher that returns geographic context."""

    def enrich(self, detection: Detection) -> Enrichment:
        return Enrichment(
            data={
                "geoip": {
                    "country": "United States",
                    "city": "Houston",
                }
            }
        )


class ThreatIntelTestEnricher(Enricher):
    """Test enricher that returns threat intelligence context."""

    def enrich(self, detection: Detection) -> Enrichment:
        return Enrichment(
            data={
                "threat_intel": {
                    "malicious": False,
                    "source": "test",
                }
            }
        )


def create_test_detection() -> Detection:
    """Create a reusable detection for enrichment tests."""

    return Detection(
        rule_id="AUTH-001",
        title="Windows Failed Login",
        severity=Severity.MEDIUM,
        event=Event(
            timestamp="2026-10-08T12:00:00Z",
            log_source="windows",
            event_type=EventType.AUTHENTICATION_FAILED,
            message="Failed login attempt",
            raw_message="Sample Windows failed login event",
        ),
    )


def test_enrichment_engine_with_no_enrichers_returns_empty_enrichment():
    detection = create_test_detection()
    engine = EnrichmentEngine([])

    result = engine.process(detection)

    assert result.enrichment.data == {}
    assert result.detection is detection


def test_enrichment_engine_with_one_enricher_adds_its_data():
    detection = create_test_detection()
    engine = EnrichmentEngine([GeoIPTestEnricher()])

    result = engine.process(detection)

    assert result.enrichment.data == {
        "geoip": {
            "country": "United States",
            "city": "Houston",
        }
    }
    assert result.detection is detection


def test_enrichment_engine_merges_data_from_multiple_enrichers():
    detection = create_test_detection()
    engine = EnrichmentEngine(
        [
            GeoIPTestEnricher(),
            ThreatIntelTestEnricher(),
        ]
    )

    result = engine.process(detection)

    assert result.enrichment.data == {
        "geoip": {
            "country": "United States",
            "city": "Houston",
        },
        "threat_intel": {
            "malicious": False,
            "source": "test",
        },
    }


def test_enrichment_engine_preserves_original_detection():
    detection = create_test_detection()
    engine = EnrichmentEngine([GeoIPTestEnricher()])

    result = engine.process(detection)

    assert result.detection is detection