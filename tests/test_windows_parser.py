from normalization.windows import WindowsParser
from common import event_types

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
