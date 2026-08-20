from datetime import datetime, timezone

import pytest
from sqlmodel import Session, select

from domain.entities.raw_organisme import RawOrganisme
from infrastructure.models.raw_organisme import RawOrganismeModel
from infrastructure.raw_organisme_repository import (
    RawOrganismeRepository,  # noqa: F401 — used via shared fixture
)

pytestmark = pytest.mark.usefixtures("clean_db")

REFERENTIEL = "FINESS"
EXTERNAL_ID = "123456789"


def _fetch(db_engine, referentiel: str, external_id: str) -> RawOrganismeModel | None:
    with Session(db_engine) as session:
        return session.exec(
            select(RawOrganismeModel).where(
                RawOrganismeModel.referentiel == referentiel,
                RawOrganismeModel.external_id == external_id,
            )
        ).first()


@pytest.mark.asyncio
async def test_upsert_batch_inserts_new_organismes(raw_organisme_repository, db_engine):
    organisme = RawOrganisme(
        referentiel=REFERENTIEL,
        millesime="2026-08-19",
        external_id=EXTERNAL_ID,
        data={"nom": "Hôpital Test"},
        loaded_at=datetime.now(tz=timezone.utc),
    )

    await raw_organisme_repository.upsert_batch([organisme])

    saved = _fetch(db_engine, REFERENTIEL, EXTERNAL_ID)
    assert saved is not None
    assert saved.id == organisme.id
    assert saved.referentiel == REFERENTIEL
    assert saved.millesime == "2026-08-19"
    assert saved.external_id == EXTERNAL_ID
    assert saved.data == {"nom": "Hôpital Test"}
    assert saved.loaded_at is not None
    assert saved.error_msg is None


@pytest.mark.asyncio
async def test_upsert_batch_inserts_multiple_organismes_in_one_call(
    raw_organisme_repository, db_engine
):
    organismes = [
        RawOrganisme(
            referentiel=REFERENTIEL, millesime="2026-08-19", external_id=str(i)
        )
        for i in range(10)
    ]

    await raw_organisme_repository.upsert_batch(organismes)

    for i in range(10):
        assert _fetch(db_engine, REFERENTIEL, str(i)) is not None


@pytest.mark.asyncio
async def test_upsert_batch_updates_data_and_millesime_on_conflict(
    raw_organisme_repository, db_engine
):
    await raw_organisme_repository.upsert_batch(
        [
            RawOrganisme(
                referentiel=REFERENTIEL,
                millesime="2026-08-18",
                external_id=EXTERNAL_ID,
                data={"version": 1},
            )
        ]
    )

    await raw_organisme_repository.upsert_batch(
        [
            RawOrganisme(
                referentiel=REFERENTIEL,
                millesime="2026-08-19",
                external_id=EXTERNAL_ID,
                data={"version": 2},
            )
        ]
    )

    saved = _fetch(db_engine, REFERENTIEL, EXTERNAL_ID)
    assert saved.data == {"version": 2}
    assert saved.millesime == "2026-08-19"


@pytest.mark.asyncio
async def test_upsert_batch_resets_cleaned_at_on_conflict(
    raw_organisme_repository, db_engine
):
    organisme = RawOrganisme(
        referentiel=REFERENTIEL, millesime="2026-08-18", external_id=EXTERNAL_ID
    )
    await raw_organisme_repository.upsert_batch([organisme])
    await raw_organisme_repository.mark_as_cleaned_batch(
        [organisme.id], datetime.now(tz=timezone.utc)
    )
    assert _fetch(db_engine, REFERENTIEL, EXTERNAL_ID).cleaned_at is not None

    await raw_organisme_repository.upsert_batch(
        [
            RawOrganisme(
                referentiel=REFERENTIEL, millesime="2026-08-19", external_id=EXTERNAL_ID
            )
        ]
    )

    assert _fetch(db_engine, REFERENTIEL, EXTERNAL_ID).cleaned_at is None


@pytest.mark.asyncio
async def test_upsert_batch_does_not_set_cleaned_at_on_insert(
    raw_organisme_repository, db_engine
):
    organisme = RawOrganisme(
        referentiel=REFERENTIEL,
        millesime="2026-08-19",
        external_id=EXTERNAL_ID,
        cleaned_at=None,
    )

    await raw_organisme_repository.upsert_batch([organisme])

    assert _fetch(db_engine, REFERENTIEL, EXTERNAL_ID).cleaned_at is None


@pytest.mark.asyncio
async def test_upsert_batch_preserves_id_on_conflict(
    raw_organisme_repository, db_engine
):
    first = RawOrganisme(
        referentiel=REFERENTIEL, millesime="2026-08-18", external_id=EXTERNAL_ID
    )
    await raw_organisme_repository.upsert_batch([first])
    after_first = _fetch(db_engine, REFERENTIEL, EXTERNAL_ID)

    await raw_organisme_repository.upsert_batch(
        [
            RawOrganisme(
                referentiel=REFERENTIEL, millesime="2026-08-19", external_id=EXTERNAL_ID
            )
        ]
    )
    after_second = _fetch(db_engine, REFERENTIEL, EXTERNAL_ID)

    assert after_second.id == after_first.id == first.id


@pytest.mark.asyncio
async def test_upsert_batch_same_external_id_different_referentiel(
    raw_organisme_repository, db_engine
):
    await raw_organisme_repository.upsert_batch(
        [
            RawOrganisme(
                referentiel="FINESS", millesime="2026-08-19", external_id=EXTERNAL_ID
            )
        ]
    )
    await raw_organisme_repository.upsert_batch(
        [
            RawOrganisme(
                referentiel="OTHER_REF", millesime="2026-08-19", external_id=EXTERNAL_ID
            )
        ]
    )

    row1 = _fetch(db_engine, "FINESS", EXTERNAL_ID)
    row2 = _fetch(db_engine, "OTHER_REF", EXTERNAL_ID)
    assert row1 is not None
    assert row2 is not None
    assert row1.id != row2.id


@pytest.mark.asyncio
async def test_upsert_batch_with_empty_list_is_noop(
    raw_organisme_repository, db_engine
):
    await raw_organisme_repository.upsert_batch([])

    assert _fetch(db_engine, REFERENTIEL, EXTERNAL_ID) is None


@pytest.mark.asyncio
async def test_delete_missing_removes_rows_older_than_watermark(
    raw_organisme_repository, db_engine
):
    await raw_organisme_repository.upsert_batch(
        [
            RawOrganisme(
                referentiel=REFERENTIEL,
                millesime="2026-08-18",
                external_id=EXTERNAL_ID,
                loaded_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
            )
        ]
    )

    deleted = await raw_organisme_repository.delete_missing(
        REFERENTIEL, datetime(2026, 8, 19, tzinfo=timezone.utc)
    )

    assert deleted == 1
    assert _fetch(db_engine, REFERENTIEL, EXTERNAL_ID) is None


@pytest.mark.asyncio
async def test_delete_missing_keeps_rows_refreshed_by_latest_import(
    raw_organisme_repository, db_engine
):
    loaded_at = datetime(2026, 8, 19, tzinfo=timezone.utc)
    await raw_organisme_repository.upsert_batch(
        [
            RawOrganisme(
                referentiel=REFERENTIEL,
                millesime="2026-08-19",
                external_id=EXTERNAL_ID,
                loaded_at=loaded_at,
            )
        ]
    )

    deleted = await raw_organisme_repository.delete_missing(REFERENTIEL, loaded_at)

    assert deleted == 0
    assert _fetch(db_engine, REFERENTIEL, EXTERNAL_ID) is not None


@pytest.mark.asyncio
async def test_delete_missing_removes_rows_with_null_loaded_at(
    raw_organisme_repository, db_engine
):
    await raw_organisme_repository.upsert_batch(
        [
            RawOrganisme(
                referentiel=REFERENTIEL, millesime="2026-08-18", external_id=EXTERNAL_ID
            )
        ]
    )

    deleted = await raw_organisme_repository.delete_missing(
        REFERENTIEL, datetime(2026, 8, 19, tzinfo=timezone.utc)
    )

    assert deleted == 1
    assert _fetch(db_engine, REFERENTIEL, EXTERNAL_ID) is None


@pytest.mark.asyncio
async def test_delete_missing_does_not_affect_other_referentiels(
    raw_organisme_repository, db_engine
):
    await raw_organisme_repository.upsert_batch(
        [
            RawOrganisme(
                referentiel="OTHER_REF",
                millesime="2026-08-18",
                external_id=EXTERNAL_ID,
                loaded_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
            )
        ]
    )

    deleted = await raw_organisme_repository.delete_missing(
        REFERENTIEL, datetime(2026, 8, 19, tzinfo=timezone.utc)
    )

    assert deleted == 0
    assert _fetch(db_engine, "OTHER_REF", EXTERNAL_ID) is not None


@pytest.mark.asyncio
async def test_find_uncleaned_returns_only_uncleaned_rows_for_referentiel(
    raw_organisme_repository, db_engine
):
    await raw_organisme_repository.upsert_batch(
        [
            RawOrganisme(
                referentiel=REFERENTIEL, millesime="2026-08-19", external_id="uncleaned"
            ),
            RawOrganisme(
                referentiel="OTHER_REF", millesime="2026-08-19", external_id="other-ref"
            ),
        ]
    )
    cleaned = RawOrganisme(
        referentiel=REFERENTIEL, millesime="2026-08-19", external_id="cleaned"
    )
    await raw_organisme_repository.upsert_batch([cleaned])
    await raw_organisme_repository.mark_as_cleaned_batch(
        [cleaned.id], datetime.now(tz=timezone.utc)
    )

    found = await raw_organisme_repository.find_uncleaned(REFERENTIEL, limit=10)

    assert {row.external_id for row in found} == {"uncleaned"}


@pytest.mark.asyncio
async def test_find_uncleaned_respects_limit(raw_organisme_repository, db_engine):
    await raw_organisme_repository.upsert_batch(
        [
            RawOrganisme(
                referentiel=REFERENTIEL, millesime="2026-08-19", external_id=str(i)
            )
            for i in range(5)
        ]
    )

    found = await raw_organisme_repository.find_uncleaned(REFERENTIEL, limit=2)

    assert len(found) == 2


@pytest.mark.asyncio
async def test_mark_as_cleaned_batch_sets_cleaned_at(
    raw_organisme_repository, db_engine
):
    organisme = RawOrganisme(
        referentiel=REFERENTIEL, millesime="2026-08-19", external_id=EXTERNAL_ID
    )
    await raw_organisme_repository.upsert_batch([organisme])
    cleaned_at = datetime.now(tz=timezone.utc)

    await raw_organisme_repository.mark_as_cleaned_batch([organisme.id], cleaned_at)

    saved = _fetch(db_engine, REFERENTIEL, EXTERNAL_ID)
    assert saved.cleaned_at is not None


@pytest.mark.asyncio
async def test_mark_as_cleaned_batch_with_empty_ids_is_noop(
    raw_organisme_repository, db_engine
):
    organisme = RawOrganisme(
        referentiel=REFERENTIEL, millesime="2026-08-19", external_id=EXTERNAL_ID
    )
    await raw_organisme_repository.upsert_batch([organisme])

    await raw_organisme_repository.mark_as_cleaned_batch(
        [], datetime.now(tz=timezone.utc)
    )

    saved = _fetch(db_engine, REFERENTIEL, EXTERNAL_ID)
    assert saved.cleaned_at is None
