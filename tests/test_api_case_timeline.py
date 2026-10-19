from fastapi.testclient import TestClient

from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.sqlite_unit_of_work import SQLiteUnitOfWork
from tests.test_api_cases import build_case


def test_get_case_timeline(
    client: TestClient,
    connection_factory: SQLiteConnectionFactory,
) -> None:
    case = build_case()

    case.assign(
        team="Tier 2",
        assigned_by="alice",
        reason="High severity activity",
    )

    case.start_investigation(
        analyst="alice",
    )

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.cases.save(case)
        uow.commit()

    response = client.get(
        f"/cases/{case.id}/timeline",
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["timeline"]) == 3

    assert (
        body["timeline"][0]["description"]
        == "Case created."
    )

    assert (
        body["timeline"][1]["actor"]
        == "alice"
    )

    assert (
        body["timeline"][2]["actor"]
        == "alice"
    )
