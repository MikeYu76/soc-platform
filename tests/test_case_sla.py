from datetime import UTC, datetime, timedelta

from case.domain.sla import CaseSLA


def test_sla_stores_target_minutes() -> None:
    due_at = datetime.now(UTC) + timedelta(hours=4)

    sla = CaseSLA(
        target_minutes=240,
        due_at=due_at,
    )

    assert sla.target_minutes == 240


def test_sla_stores_due_date() -> None:
    due_at = datetime.now(UTC) + timedelta(hours=2)

    sla = CaseSLA(
        target_minutes=120,
        due_at=due_at,
    )

    assert sla.due_at == due_at


def test_sla_defaults_to_not_breached() -> None:
    sla = CaseSLA(
        target_minutes=60,
        due_at=datetime.now(UTC),
    )

    assert sla.breached is False


def test_sla_has_no_breach_timestamp_by_default() -> None:
    sla = CaseSLA(
        target_minutes=60,
        due_at=datetime.now(UTC),
    )

    assert sla.breached_at is None


def test_sla_can_store_breach_information() -> None:
    breached_at = datetime.now(UTC)

    sla = CaseSLA(
        target_minutes=15,
        due_at=breached_at - timedelta(minutes=15),
        breached=True,
        breached_at=breached_at,
    )

    assert sla.breached is True
    assert sla.breached_at == breached_at
