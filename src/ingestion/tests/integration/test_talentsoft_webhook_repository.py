import pytest
from sqlmodel import Session, select

from domain.entities.talentsoft_webhook import TalentsoftWebhook
from domain.value_objects.webhook_event import EventType, OfferStatus
from infrastructure.models.talentsoft_webhook import TalentsoftWebhookModel
from infrastructure.talentsoft_webhook_repository import (
    TalentsoftWebhookRepository,  # noqa: F401 — used via shared fixture
)

pytestmark = pytest.mark.usefixtures("clean_db")

SOURCE_ID = "11111111-2222-3333-4444-555555555555"
REFERENCE = "2024-WEBHOOK-001"


def _fetch(db_engine, source_id: str, reference: str) -> TalentsoftWebhookModel | None:
    with Session(db_engine) as session:
        return session.exec(
            select(TalentsoftWebhookModel).where(
                TalentsoftWebhookModel.source_id == source_id,
                TalentsoftWebhookModel.reference == reference,
            )
        ).first()


# ---------------------------------------------------------------------------
# Insert
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_insert_saves_webhook(talentsoft_webhook_repository, db_engine):
    webhook = TalentsoftWebhook(
        source_id=SOURCE_ID,
        event_type=EventType.CREE,
        reference=REFERENCE,
        payload={"event_type": str(EventType.CREE), "reference": REFERENCE},
    )

    await talentsoft_webhook_repository.insert(webhook)

    saved = _fetch(db_engine, SOURCE_ID, REFERENCE)
    assert saved is not None
    assert saved.id == webhook.id
    assert saved.source_id == SOURCE_ID
    assert saved.event_type == EventType.CREE
    assert saved.reference == REFERENCE
    assert saved.status_id is None
    assert saved.payload == {"event_type": str(EventType.CREE), "reference": REFERENCE}


@pytest.mark.asyncio
async def test_insert_saves_status_id(talentsoft_webhook_repository, db_engine):
    webhook = TalentsoftWebhook(
        source_id=SOURCE_ID,
        event_type=EventType.STATUT_CHANGE,
        reference=REFERENCE,
        payload={"event_type": str(EventType.STATUT_CHANGE), "reference": REFERENCE},
        status_id=OfferStatus.DIFFUSE,
    )

    await talentsoft_webhook_repository.insert(webhook)

    saved = _fetch(db_engine, SOURCE_ID, REFERENCE)
    assert saved.status_id == OfferStatus.DIFFUSE
    assert saved.event_type == EventType.STATUT_CHANGE


@pytest.mark.asyncio
async def test_insert_sets_timestamps(talentsoft_webhook_repository, db_engine):
    webhook = TalentsoftWebhook(
        source_id=SOURCE_ID,
        event_type=EventType.CREE,
        reference=REFERENCE,
        payload={"event_type": str(EventType.CREE), "reference": REFERENCE},
    )

    await talentsoft_webhook_repository.insert(webhook)

    saved = _fetch(db_engine, SOURCE_ID, REFERENCE)
    assert saved.created_at is not None
    assert saved.updated_at is not None


# ---------------------------------------------------------------------------
# Uniqueness
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_insert_allows_multiple_event_types_for_same_reference(
    talentsoft_webhook_repository, db_engine
):
    for event_type in (EventType.CREE, EventType.MIS_A_JOUR, EventType.SUPPRIME):
        await talentsoft_webhook_repository.insert(
            TalentsoftWebhook(
                source_id=SOURCE_ID,
                event_type=event_type,
                reference=REFERENCE,
                payload={"event_type": str(event_type), "reference": REFERENCE},
            )
        )

    with Session(db_engine) as session:
        rows = session.exec(
            select(TalentsoftWebhookModel).where(
                TalentsoftWebhookModel.source_id == SOURCE_ID,
                TalentsoftWebhookModel.reference == REFERENCE,
            )
        ).all()
    assert len(rows) == 3


@pytest.mark.asyncio
async def test_insert_allows_same_reference_different_source_ids(
    talentsoft_webhook_repository, db_engine
):
    payload = {"event_type": str(EventType.CREE), "reference": REFERENCE}
    first = TalentsoftWebhook(
        source_id=SOURCE_ID,
        event_type=EventType.CREE,
        reference=REFERENCE,
        payload=payload,
    )
    second = TalentsoftWebhook(
        source_id="other-source-id",
        event_type=EventType.CREE,
        reference=REFERENCE,
        payload=payload,
    )

    await talentsoft_webhook_repository.insert(first)
    await talentsoft_webhook_repository.insert(second)

    row1 = _fetch(db_engine, SOURCE_ID, REFERENCE)
    row2 = _fetch(db_engine, "other-source-id", REFERENCE)
    assert row1 is not None
    assert row2 is not None
    assert row1.id != row2.id


@pytest.mark.asyncio
async def test_insert_allows_same_source_id_different_references(
    talentsoft_webhook_repository, db_engine
):
    first = TalentsoftWebhook(
        source_id=SOURCE_ID,
        event_type=EventType.CREE,
        reference=REFERENCE,
        payload={"event_type": str(EventType.CREE), "reference": REFERENCE},
    )
    second = TalentsoftWebhook(
        source_id=SOURCE_ID,
        event_type=EventType.CREE,
        reference="OTHER-REF",
        payload={"event_type": str(EventType.CREE), "reference": "OTHER-REF"},
    )

    await talentsoft_webhook_repository.insert(first)
    await talentsoft_webhook_repository.insert(second)

    row1 = _fetch(db_engine, SOURCE_ID, REFERENCE)
    row2 = _fetch(db_engine, SOURCE_ID, "OTHER-REF")
    assert row1 is not None
    assert row2 is not None
    assert row1.id != row2.id
