from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_process_security_event() -> None:
    payload = {
        "event": {
            "timestamp": "2026-01-01T00:00:00Z",
            "log_source": "windows",
            "event_type": "authentication_failed",
            "message": "Failed login",
            "raw_message": "User admin failed to log in.",
            "hostname": "dc01",
            "username": "admin",
            "source_ip": "8.8.8.8",
            "destination_ip": "10.0.0.5",
        }
    }

    response = client.post("/events", json=payload)

    assert response.status_code == 200

    body = response.json()

    assert "event" in body
    assert "detections" in body
    assert "enriched_detections" in body
    assert "correlations" in body
    assert "alerts" in body
    assert "cases" in body

    event = body["event"]

    assert event["log_source"] == "windows"
    assert event["event_type"] == "authentication_failed"
    assert event["message"] == "Failed login"
    assert event["raw_message"] == "User admin failed to log in."