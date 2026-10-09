
import pytest

from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType
from risk.engine import RiskEngine
from risk.models import RiskAssessment


def create_test_detection(severity: Severity) -> Detection:
    """Create a detection with a configurable severity."""
    return Detection(
        rule_id="AUTH-001",
        title="Windows Failed Login",
        severity=severity,
        event=Event(
            timestamp="2026-10-08T12:00:00Z",
            log_source="windows",
            event_type=EventType.AUTHENTICATION_FAILED,
            message="Failed login attempt",
            raw_message="Sample Windows failed login event",
        ),
    )


@pytest.mark.parametrize(
    ("severity", "expected_score"),
    [
        (Severity.LOW, 25),
        (Severity.MEDIUM, 50),
        (Severity.HIGH, 75),
        (Severity.CRITICAL, 100),
    ],
)
def test_risk_engine_scores_detection_by_severity(
    severity: Severity,
    expected_score: int,
):
    detection = create_test_detection(severity)
    engine = RiskEngine()

    result = engine.assess(detection)

    assert result.score == expected_score
    assert result.severity == severity.value
    assert result.detection_id == detection.detection_id


def test_risk_engine_provides_reasoning():
    detection = create_test_detection(Severity.HIGH)
    engine = RiskEngine()

    result = engine.assess(detection)

    assert result.reasoning == (
        "Base risk score of 75 assigned for high severity."
    )


@pytest.mark.parametrize("invalid_score", [-1, 101])
def test_risk_assessment_rejects_scores_outside_valid_range(
    invalid_score: int,
):
    with pytest.raises(ValueError):
        RiskAssessment(
            detection_id="test-detection",
            score=invalid_score,
            severity="high",
            reasoning="Test validation",
        )