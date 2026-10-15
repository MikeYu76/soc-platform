from fastapi.testclient import TestClient


def test_list_alerts(
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

    process_response = client.post(
        "/events",
        json=payload,
    )

    assert process_response.status_code == 200
    print(process_response.json())

    response = client.get("/alerts")

    assert response.status_code == 200

    body = response.json()

    assert "alerts" in body
    assert body["alerts"] == []