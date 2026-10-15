from uuid import uuid4

from alert.models import Alert
from alert.processing.grouping import AlertGroupingProcessor
from common.detection import Detection
from common.event import Event
from common.event_types import EventType
from common.detection import Detection, Severity

def make_detection(title: str = "Detection") -> Detection:
    event = Event(
        timestamp="2025-01-01T00:00:00Z",
        log_source="windows",
        event_type=EventType.AUTHENTICATION_FAILED,
        message="Failed login",
        raw_message="4625 Failed login",
    )

    return Detection(
        rule_id="rule",
        title=title,
        severity=Severity.HIGH,
        event=event,
    )


def make_alert(title: str) -> Alert:
    detection = make_detection(title)

    return Alert(
        title=title,
        severity=Severity.HIGH,
        source=detection,
    )


def test_groups_alerts_with_same_title():
    processor = AlertGroupingProcessor()

    alert1 = make_alert("Failed Login")
    alert2 = make_alert("Failed Login")
    alert3 = make_alert("Impossible Travel")

    result = processor.process([alert1, alert2, alert3])

    assert len(result) == 2

    grouped = result[0]

    assert grouped.title == "Failed Login"
    assert "grouped_ids" in grouped.metadata
    assert len(grouped.metadata["grouped_ids"]) == 2


def test_keeps_first_alert_as_group_representative():
    processor = AlertGroupingProcessor()

    alert1 = make_alert("Failed Login")
    alert2 = make_alert("Failed Login")

    result = processor.process([alert1, alert2])

    assert result[0].id == alert1.id


def test_single_alert_is_not_modified():
    processor = AlertGroupingProcessor()

    alert = make_alert("Single Alert")

    result = processor.process([alert])

    assert len(result) == 1
    assert result[0].metadata == {}


def test_different_titles_are_not_grouped():
    processor = AlertGroupingProcessor()

    alerts = [
        make_alert("A"),
        make_alert("B"),
        make_alert("C"),
    ]

    result = processor.process(alerts)

    assert len(result) == 3


def test_group_contains_all_ids():
    processor = AlertGroupingProcessor()

    alerts = [
        make_alert("Failed Login"),
        make_alert("Failed Login"),
        make_alert("Failed Login"),
    ]

    result = processor.process(alerts)

    ids = result[0].metadata["grouped_ids"]

    assert len(ids) == 3

    expected = {alert.id for alert in alerts}

    assert set(ids) == expected