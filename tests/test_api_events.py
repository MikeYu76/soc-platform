from fastapi.testclient import TestClient


def test_process_security_event(
    client: TestClient,
) -> None:
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

    response = client.post(
        "/events",
        json=payload,
    )

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


def test_list_events(
    client: TestClient,
) -> None:
    response = client.get("/events")

    assert response.status_code == 200

    body = response.json()

    assert "events" in body
    assert isinstance(body["events"], list)


def test_get_event(
    client: TestClient,
) -> None:
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

    create_response = client.post(
        "/events",
        json=payload,
    )

    assert create_response.status_code == 200

    event = create_response.json()["event"]

    response = client.get(
        f"/events/{event['id']}",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["event"]["id"] == event["id"]
    assert body["event"]["message"] == "Failed login"

def test_get_missing_event(
    client: TestClient,
) -> None:
    response = client.get(
        "/events/DOES-NOT-EXIST",
    )

    assert response.status_code == 404

    body = response.json()

    assert "detail" in body    