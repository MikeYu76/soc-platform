from datetime import UTC, datetime

from common.detection import Severity
from correlation.base import CorrelationRule
from correlation.engine import CorrelationEngine
from correlation.models import CorrelationResult
from enrichment.models import EnrichedDetection


class NoMatchRule(CorrelationRule):
    def correlate(
        self,
        detections: list[EnrichedDetection],
    ) -> list[CorrelationResult]:
        return []


class MatchRule(CorrelationRule):
    def correlate(
        self,
        detections: list[EnrichedDetection],
    ) -> list[CorrelationResult]:
        return [
            CorrelationResult(
                correlation_id="corr-001",
                rule_id="TEST-001",
                title="Test Correlation",
                severity=Severity.HIGH,
                matched_at=datetime.now(UTC),
                detections=[],
                metadata={},
            )
        ]


def test_correlation_engine_with_no_rules_returns_empty_list():
    engine = CorrelationEngine([])

    results = engine.correlate([])

    assert results == []


def test_correlation_engine_with_no_matches_returns_empty_list():
    engine = CorrelationEngine([NoMatchRule()])

    results = engine.correlate([])

    assert results == []


def test_correlation_engine_returns_matches():
    engine = CorrelationEngine([MatchRule()])

    results = engine.correlate([])

    assert len(results) == 1
    assert results[0].rule_id == "TEST-001"


def test_correlation_engine_runs_multiple_rules():
    engine = CorrelationEngine(
        [
            MatchRule(),
            MatchRule(),
        ]
    )

    results = engine.correlate([])

    assert len(results) == 2