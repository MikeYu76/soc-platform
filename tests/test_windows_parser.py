from common.event_types import EventType
from normalization.windows import WindowsParser


def test_maps_failed_login_event():
    raw_log = {
        "EventID": 4625,
        "TimeCreated": "2026-10-05T10:15:30Z",
        "Computer": "DC01",
        "TargetUserName": "administrator",
        "IpAddress": "192.168.1.50",
        "Message": "An account failed to log on.",
    }

    parser = WindowsParser()
    event = parser.parse(raw_log)

    assert event.event_type == EventType.AUTHENTICATION_FAILED
    assert event.hostname == "DC01"
    assert event.username == "administrator"
    assert str(event.source_ip) == "192.168.1.50"
    assert event.event_id == 4625
