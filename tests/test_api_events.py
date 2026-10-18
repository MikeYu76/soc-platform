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


def test_filter_events_by_hostname(
    client: TestClient,
) -> None:
    payloads = [
        {
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
        },
        {
            "event": {
                "timestamp": "2026-01-01T00:01:00Z",
                "log_source": "windows",
                "event_type": "authentication_failed",
                "message": "Failed login",
                "raw_message": "User guest failed to log in.",
                "hostname": "web01",
                "username": "guest",
                "source_ip": "1.1.1.1",
                "destination_ip": "10.0.0.10",
            }
        },
    ]

    for payload in payloads:
        response = client.post(
            "/events",
            json=payload,
        )

        assert response.status_code == 200

    response = client.get(
        "/events",
        params={
            "hostname": "dc01",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["events"]) == 1
    assert body["events"][0]["hostname"] == "dc01"


def test_filter_events_by_event_type(
    client: TestClient,
) -> None:
    payloads = [
        {
            "event": {
                "timestamp": "2026-01-01T00:00:00Z",
                "log_source": "windows",
                "event_type": "authentication_failed",
                "message": "Failed login",
                "raw_message": "Authentication failure.",
                "hostname": "dc01",
                "username": "admin",
                "source_ip": "8.8.8.8",
                "destination_ip": "10.0.0.5",
            }
        },
        {
            "event": {
                "timestamp": "2026-01-01T00:01:00Z",
                "log_source": "windows",
                "event_type": "process_created",
                "message": "Process started",
                "raw_message": "cmd.exe launched.",
                "hostname": "dc01",
                "username": "admin",
                "source_ip": "8.8.8.8",
                "destination_ip": "10.0.0.5",
            }
        },
    ]

    for payload in payloads:
        response = client.post(
            "/events",
            json=payload,
        )

        assert response.status_code == 200

    response = client.get(
        "/events",
        params={
            "event_type": "authentication_failed",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["events"]) == 1
    assert body["events"][0]["event_type"] == "authentication_failed"


def test_filter_events_by_username(
    client: TestClient,
) -> None:
    payloads = [
        {
            "event": {
                "timestamp": "2026-01-01T00:00:00Z",
                "log_source": "windows",
                "event_type": "authentication_failed",
                "message": "Failed login",
                "raw_message": "Administrator failed login.",
                "hostname": "dc01",
                "username": "administrator",
                "source_ip": "8.8.8.8",
                "destination_ip": "10.0.0.5",
            }
        },
        {
            "event": {
                "timestamp": "2026-01-01T00:01:00Z",
                "log_source": "windows",
                "event_type": "authentication_failed",
                "message": "Failed login",
                "raw_message": "Guest failed login.",
                "hostname": "dc01",
                "username": "guest",
                "source_ip": "1.1.1.1",
                "destination_ip": "10.0.0.5",
            }
        },
    ]

    for payload in payloads:
        response = client.post(
            "/events",
            json=payload,
        )

        assert response.status_code == 200

    response = client.get(
        "/events",
        params={
            "username": "administrator",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["events"]) == 1
    assert body["events"][0]["username"] == "administrator"


def test_filter_events_by_log_source(
    client: TestClient,
) -> None:
    payloads = [
        {
            "event": {
                "timestamp": "2026-01-01T00:00:00Z",
                "log_source": "windows",
                "event_type": "authentication_failed",
                "message": "Windows failed login",
                "raw_message": "Windows authentication failure.",
                "hostname": "dc01",
                "username": "administrator",
                "source_ip": "8.8.8.8",
                "destination_ip": "10.0.0.5",
            }
        },
        {
            "event": {
                "timestamp": "2026-01-01T00:01:00Z",
                "log_source": "linux",
                "event_type": "authentication_failed",
                "message": "Linux failed login",
                "raw_message": "Linux authentication failure.",
                "hostname": "web01",
                "username": "root",
                "source_ip": "1.1.1.1",
                "destination_ip": "10.0.0.10",
            }
        },
    ]

    for payload in payloads:
        response = client.post(
            "/events",
            json=payload,
        )

        assert response.status_code == 200

    response = client.get(
        "/events",
        params={
            "log_source": "windows",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["events"]) == 1
    assert body["events"][0]["log_source"] == "windows"


def test_filter_events_by_source_ip(
    client: TestClient,
) -> None:
    payloads = [
        {
            "event": {
                "timestamp": "2026-01-01T00:00:00Z",
                "log_source": "windows",
                "event_type": "authentication_failed",
                "message": "Failed login",
                "raw_message": "Administrator failed login.",
                "hostname": "dc01",
                "username": "administrator",
                "source_ip": "8.8.8.8",
                "destination_ip": "10.0.0.5",
            }
        },
        {
            "event": {
                "timestamp": "2026-01-01T00:01:00Z",
                "log_source": "windows",
                "event_type": "authentication_failed",
                "message": "Failed login",
                "raw_message": "Guest failed login.",
                "hostname": "dc01",
                "username": "guest",
                "source_ip": "1.1.1.1",
                "destination_ip": "10.0.0.5",
            }
        },
    ]

    for payload in payloads:
        response = client.post(
            "/events",
            json=payload,
        )

        assert response.status_code == 200

    response = client.get(
        "/events",
        params={
            "source_ip": "8.8.8.8",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["events"]) == 1
    assert body["events"][0]["source_ip"] == "8.8.8.8"


def test_filter_events_by_destination_ip(
    client: TestClient,
) -> None:
    payloads = [
        {
            "event": {
                "timestamp": "2026-01-01T00:00:00Z",
                "log_source": "windows",
                "event_type": "authentication_failed",
                "message": "Failed login",
                "raw_message": "Administrator failed login.",
                "hostname": "dc01",
                "username": "administrator",
                "source_ip": "8.8.8.8",
                "destination_ip": "10.0.0.5",
            }
        },
        {
            "event": {
                "timestamp": "2026-01-01T00:01:00Z",
                "log_source": "windows",
                "event_type": "authentication_failed",
                "message": "Failed login",
                "raw_message": "Guest failed login.",
                "hostname": "dc01",
                "username": "guest",
                "source_ip": "1.1.1.1",
                "destination_ip": "10.0.0.10",
            }
        },
    ]

    for payload in payloads:
        response = client.post(
            "/events",
            json=payload,
        )

        assert response.status_code == 200

    response = client.get(
        "/events",
        params={
            "destination_ip": "10.0.0.5",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["events"]) == 1
    assert body["events"][0]["destination_ip"] == "10.0.0.5"


def test_limit_events(
    client: TestClient,
) -> None:
    for i in range(3):
        payload = {
            "event": {
                "timestamp": f"2026-01-01T00:00:0{i}Z",
                "log_source": "windows",
                "event_type": "authentication_failed",
                "message": f"Failed login {i}",
                "raw_message": f"Failed login {i}",
                "hostname": f"dc0{i}",
                "username": f"user{i}",
                "source_ip": f"8.8.8.{i + 1}",
                "destination_ip": "10.0.0.5",
            }
        }

        response = client.post(
            "/events",
            json=payload,
        )

        assert response.status_code == 200

    response = client.get(
        "/events",
        params={
            "limit": 2,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["events"]) == 2


def test_offset_events(
    client: TestClient,
) -> None:
    created = []

    for i in range(3):
        payload = {
            "event": {
                "timestamp": f"2026-01-01T00:00:0{i}Z",
                "log_source": "offset-test",
                "event_type": "authentication_failed",
                "message": f"Event {i}",
                "raw_message": f"Event {i}",
                "hostname": "offset-host",
                "username": f"offset-user{i}",
                "source_ip": f"8.8.8.{i + 1}",
                "destination_ip": "10.0.0.5",
            }
        }

        response = client.post(
            "/events",
            json=payload,
        )

        assert response.status_code == 200

        created.append(response.json()["event"])

    response = client.get(
        "/events",
        params={
            "log_source": "offset-test",
            "limit": 2,
            "offset": 1,
            "sort_by": "timestamp",
            "order": "desc",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["events"]) == 2

    assert body["events"][0]["username"] == "offset-user1"
    assert body["events"][1]["username"] == "offset-user0"


def test_sort_events_by_username(
    client: TestClient,
) -> None:
    payloads = [
        {
            "event": {
                "timestamp": "2026-01-01T00:00:00Z",
                "log_source": "sort-test",
                "event_type": "authentication_failed",
                "message": "Event",
                "raw_message": "Event",
                "hostname": "dc01",
                "username": "charlie",
                "source_ip": "8.8.8.8",
                "destination_ip": "10.0.0.5",
            }
        },
        {
            "event": {
                "timestamp": "2026-01-01T00:00:01Z",
                "log_source": "sort-test",
                "event_type": "authentication_failed",
                "message": "Event",
                "raw_message": "Event",
                "hostname": "dc01",
                "username": "alice",
                "source_ip": "1.1.1.1",
                "destination_ip": "10.0.0.5",
            }
        },
        {
            "event": {
                "timestamp": "2026-01-01T00:00:02Z",
                "log_source": "sort-test",
                "event_type": "authentication_failed",
                "message": "Event",
                "raw_message": "Event",
                "hostname": "dc01",
                "username": "bob",
                "source_ip": "9.9.9.9",
                "destination_ip": "10.0.0.5",
            }
        },
    ]

    for payload in payloads:
        response = client.post(
            "/events",
            json=payload,
        )

        assert response.status_code == 200

    response = client.get(
        "/events",
        params={
            "log_source": "sort-test",
            "sort_by": "username",
            "order": "asc",
        },
    )

    assert response.status_code == 200

    usernames = [event["username"] for event in response.json()["events"]]

    assert usernames == [
        "alice",
        "bob",
        "charlie",
    ]


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
