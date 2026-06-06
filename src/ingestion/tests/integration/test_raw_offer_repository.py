from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlmodel import Session, select

from domain.entities.raw_offer import RawOffer
from infrastructure.models.raw_offer import RawOfferModel
from infrastructure.raw_offer_repository import (
    RawOfferRepository,  # noqa: F401 — used via shared fixture
)

pytestmark = pytest.mark.usefixtures("clean_db")

REFERENCE = "2024-OFFER-001"
SOURCE_ID = "11111111-2222-3333-4444-555555555555"


def _fetch(db_engine, reference: str, source_id: str) -> RawOfferModel | None:
    with Session(db_engine) as session:
        return session.exec(
            select(RawOfferModel).where(
                RawOfferModel.reference == reference,
                RawOfferModel.source_id == source_id,
            )
        ).first()


# ---------------------------------------------------------------------------
# Insert
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_upsert_inserts_new_offer(repository, db_engine):
    offer = RawOffer(
        reference=REFERENCE,
        source_id=SOURCE_ID,
        data={"title": "Software Engineer"},
        loaded_at=datetime.now(tz=timezone.utc),
    )

    await repository.upsert(offer)

    saved = _fetch(db_engine, REFERENCE, SOURCE_ID)
    assert saved is not None
    assert saved.id == offer.id
    assert saved.reference == REFERENCE
    assert saved.source_id == SOURCE_ID
    assert saved.data == {"title": "Software Engineer"}
    assert saved.loaded_at is not None
    assert saved.error_msg is None


@pytest.mark.asyncio
async def test_upsert_stores_error_state(repository, db_engine):
    offer = RawOffer(
        reference=REFERENCE,
        source_id=SOURCE_ID,
        data=None,
        error_msg="API timeout after 30s",
        loaded_at=None,
    )

    await repository.upsert(offer)

    saved = _fetch(db_engine, REFERENCE, SOURCE_ID)
    assert saved.data is None
    assert saved.error_msg == "API timeout after 30s"
    assert saved.loaded_at is None


# ---------------------------------------------------------------------------
# Upsert on conflict
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_upsert_updates_data_on_conflict(repository, db_engine):
    first = RawOffer(
        reference=REFERENCE,
        source_id=SOURCE_ID,
        data={"version": 1},
        loaded_at=datetime.now(tz=timezone.utc),
    )
    await repository.upsert(first)

    second = RawOffer(
        reference=REFERENCE,
        source_id=SOURCE_ID,
        data={"version": 2},
        loaded_at=datetime.now(tz=timezone.utc),
    )
    await repository.upsert(second)

    saved = _fetch(db_engine, REFERENCE, SOURCE_ID)
    assert saved.data == {"version": 2}


@pytest.mark.asyncio
async def test_upsert_preserves_id_and_created_at_on_conflict(repository, db_engine):
    first = RawOffer(reference=REFERENCE, source_id=SOURCE_ID, data={"v": 1})
    await repository.upsert(first)
    after_first = _fetch(db_engine, REFERENCE, SOURCE_ID)

    second = RawOffer(reference=REFERENCE, source_id=SOURCE_ID, data={"v": 2})
    await repository.upsert(second)
    after_second = _fetch(db_engine, REFERENCE, SOURCE_ID)

    # Both values are read from the DB (naive datetimes), so comparison is safe.
    assert after_second.id == after_first.id
    assert after_second.created_at == after_first.created_at


@pytest.mark.asyncio
async def test_upsert_updates_error_msg_on_conflict(repository, db_engine):
    await repository.upsert(
        RawOffer(
            reference=REFERENCE,
            source_id=SOURCE_ID,
            data={"key": "value"},
            loaded_at=datetime.now(tz=timezone.utc),
        )
    )

    await repository.upsert(
        RawOffer(
            reference=REFERENCE,
            source_id=SOURCE_ID,
            data=None,
            error_msg="Upstream 503",
            loaded_at=None,
        )
    )

    saved = _fetch(db_engine, REFERENCE, SOURCE_ID)
    assert saved.data is None
    assert saved.error_msg == "Upstream 503"
    assert saved.loaded_at is None


@pytest.mark.asyncio
async def test_upsert_does_not_overwrite_cleaned_at_on_conflict(repository, db_engine):
    """cleaned_at is not in the ON CONFLICT SET clause, so it must survive updates."""
    await repository.upsert(
        RawOffer(
            reference=REFERENCE,
            source_id=SOURCE_ID,
            data={"v": 1},
            cleaned_at=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        )
    )
    after_first = _fetch(db_engine, REFERENCE, SOURCE_ID)

    await repository.upsert(
        RawOffer(
            reference=REFERENCE,
            source_id=SOURCE_ID,
            data={"v": 2},
            cleaned_at=None,
        )
    )
    after_second = _fetch(db_engine, REFERENCE, SOURCE_ID)

    # Both values are read from the DB (naive datetimes), so comparison is safe.
    assert after_second.cleaned_at is not None
    assert after_second.cleaned_at == after_first.cleaned_at


# ---------------------------------------------------------------------------
# mark_as_cleaned
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_mark_as_cleaned_sets_cleaned_at(repository, db_engine):
    await repository.upsert(RawOffer(reference=REFERENCE, source_id=SOURCE_ID))

    cleaned_at = datetime(2025, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    await repository.mark_as_cleaned(REFERENCE, SOURCE_ID, cleaned_at)

    saved = _fetch(db_engine, REFERENCE, SOURCE_ID)
    assert saved.cleaned_at is not None
    assert saved.cleaned_at.replace(tzinfo=timezone.utc) == cleaned_at


@pytest.mark.asyncio
async def test_mark_as_cleaned_updates_updated_at(repository, db_engine):
    await repository.upsert(RawOffer(reference=REFERENCE, source_id=SOURCE_ID))
    before = _fetch(db_engine, REFERENCE, SOURCE_ID)

    cleaned_at = datetime.now(tz=timezone.utc)
    await repository.mark_as_cleaned(REFERENCE, SOURCE_ID, cleaned_at)

    after = _fetch(db_engine, REFERENCE, SOURCE_ID)
    assert after.updated_at >= before.updated_at


@pytest.mark.asyncio
async def test_mark_as_cleaned_does_not_affect_other_rows(repository, db_engine):
    other_source_id = str(uuid4())
    await repository.upsert(RawOffer(reference=REFERENCE, source_id=SOURCE_ID))
    await repository.upsert(RawOffer(reference=REFERENCE, source_id=other_source_id))

    await repository.mark_as_cleaned(
        REFERENCE, SOURCE_ID, datetime.now(tz=timezone.utc)
    )

    other = _fetch(db_engine, REFERENCE, other_source_id)
    assert other.cleaned_at is None


@pytest.mark.asyncio
async def test_mark_as_cleaned_raises_when_row_not_found(repository, db_engine):
    with pytest.raises(ValueError, match="RawOffer not found"):
        await repository.mark_as_cleaned(
            "UNKNOWN-REF", SOURCE_ID, datetime.now(tz=timezone.utc)
        )


# ---------------------------------------------------------------------------
# mark_as_upserted
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_mark_as_upserted_sets_upsert_at(repository, db_engine):
    await repository.upsert(RawOffer(reference=REFERENCE, source_id=SOURCE_ID))

    upsert_at = datetime(2025, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    await repository.mark_as_upserted(REFERENCE, SOURCE_ID, upsert_at)

    saved = _fetch(db_engine, REFERENCE, SOURCE_ID)
    assert saved.upsert_at is not None
    assert saved.upsert_at.replace(tzinfo=timezone.utc) == upsert_at


@pytest.mark.asyncio
async def test_mark_as_upserted_updates_updated_at(repository, db_engine):
    await repository.upsert(RawOffer(reference=REFERENCE, source_id=SOURCE_ID))
    before = _fetch(db_engine, REFERENCE, SOURCE_ID)

    await repository.mark_as_upserted(
        REFERENCE, SOURCE_ID, datetime.now(tz=timezone.utc)
    )

    after = _fetch(db_engine, REFERENCE, SOURCE_ID)
    assert after.updated_at >= before.updated_at


@pytest.mark.asyncio
async def test_mark_as_upserted_does_not_affect_other_rows(repository, db_engine):
    other_source_id = str(uuid4())
    await repository.upsert(RawOffer(reference=REFERENCE, source_id=SOURCE_ID))
    await repository.upsert(RawOffer(reference=REFERENCE, source_id=other_source_id))

    await repository.mark_as_upserted(
        REFERENCE, SOURCE_ID, datetime.now(tz=timezone.utc)
    )

    other = _fetch(db_engine, REFERENCE, other_source_id)
    assert other.upsert_at is None


@pytest.mark.asyncio
async def test_mark_as_upserted_raises_when_row_not_found(repository, db_engine):
    with pytest.raises(ValueError, match="RawOffer not found"):
        await repository.mark_as_upserted(
            "UNKNOWN-REF", SOURCE_ID, datetime.now(tz=timezone.utc)
        )


# ---------------------------------------------------------------------------
# mark_as_archived
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_mark_as_archived_sets_archived_at(repository, db_engine):
    await repository.upsert(RawOffer(reference=REFERENCE, source_id=SOURCE_ID))

    archived_at = datetime(2025, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    await repository.mark_as_archived(REFERENCE, SOURCE_ID, archived_at)

    saved = _fetch(db_engine, REFERENCE, SOURCE_ID)
    assert saved.archived_at is not None
    assert saved.archived_at.replace(tzinfo=timezone.utc) == archived_at


@pytest.mark.asyncio
async def test_mark_as_archived_updates_updated_at(repository, db_engine):
    await repository.upsert(RawOffer(reference=REFERENCE, source_id=SOURCE_ID))
    before = _fetch(db_engine, REFERENCE, SOURCE_ID)

    archived_at = datetime.now(tz=timezone.utc)
    await repository.mark_as_archived(REFERENCE, SOURCE_ID, archived_at)

    after = _fetch(db_engine, REFERENCE, SOURCE_ID)
    assert after.updated_at >= before.updated_at


@pytest.mark.asyncio
async def test_mark_as_archived_does_not_affect_other_rows(repository, db_engine):
    other_source_id = str(uuid4())
    await repository.upsert(RawOffer(reference=REFERENCE, source_id=SOURCE_ID))
    await repository.upsert(RawOffer(reference=REFERENCE, source_id=other_source_id))

    await repository.mark_as_archived(
        REFERENCE, SOURCE_ID, datetime.now(tz=timezone.utc)
    )

    other = _fetch(db_engine, REFERENCE, other_source_id)
    assert other.archived_at is None


@pytest.mark.asyncio
async def test_mark_as_archived_is_noop_when_row_not_found(repository, db_engine):
    await repository.mark_as_archived(
        "UNKNOWN-REF", SOURCE_ID, datetime.now(tz=timezone.utc)
    )


# ---------------------------------------------------------------------------
# Uniqueness
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_upsert_same_reference_different_source_ids(repository, db_engine):
    other_source_id = str(uuid4())

    await repository.upsert(RawOffer(reference=REFERENCE, source_id=SOURCE_ID))
    await repository.upsert(RawOffer(reference=REFERENCE, source_id=other_source_id))

    row1 = _fetch(db_engine, REFERENCE, SOURCE_ID)
    row2 = _fetch(db_engine, REFERENCE, other_source_id)
    assert row1 is not None
    assert row2 is not None
    assert row1.id != row2.id
