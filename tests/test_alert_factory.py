from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from alert.factory import AlertFactory
from alert.models import Alert
from common.alert_status import AlertStatus
from common.detection import Severity
from correlation.models import CorrelationResult


def build_correlation_result() -> CorrelationResult:
    return CorrelationResult(
        correlation_id="corr-001",
        rule_id="CORR-001",
        title="Suspicious Authentication Activity",
        severity=Severity.HIGH,
        matched_at=datetime.now(UTC),
        detections=[],
        metadata={},
    )


def test_alert_factory_creates_alert() -> None:
    # Arrange
    factory = AlertFactory()
    correlation = build_correlation_result()

    # Act
    alert = factory.create(correlation)

    # Assert
    assert isinstance(alert, Alert)
    assert alert.title == correlation.title
    assert alert.severity == correlation.severity
    assert alert.source == correlation


def test_alert_factory_generates_id() -> None:
    # Arrange
    factory = AlertFactory()
    correlation = build_correlation_result()

    # Act
    alert = factory.create(correlation)

    # Assert
    assert isinstance(alert.id, UUID)


def test_alert_factory_sets_default_values() -> None:
    # Arrange
    factory = AlertFactory()
    correlation = build_correlation_result()

    # Act
    alert = factory.create(correlation)

    # Assert
    assert alert.status == AlertStatus.NEW
    assert alert.metadata == {}
    assert alert.created_at is not None
