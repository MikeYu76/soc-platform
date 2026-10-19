from application.dto.identifier import IdentifierRequest
from application.services.get_case_timeline import (
    GetCaseTimelineService,
)
from infrastructure.sqlite.sqlite_unit_of_work import (
    SQLiteUnitOfWork,
)
from tests.test_api_cases import build_case


def test_get_case_timeline(
    connection_factory,
) -> None:
    """
    The service should return the complete timeline
    for a persisted case.
    """

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

    service = GetCaseTimelineService(
        lambda: SQLiteUnitOfWork(connection_factory),
    )

    response = service.execute(
        IdentifierRequest(
            id=case.id,
        )
    )

    assert len(response.timeline) == 3
    assert response.timeline[0].description == "Case created."
    assert response.timeline[1].actor == "alice"
    assert response.timeline[2].actor == "alice"
