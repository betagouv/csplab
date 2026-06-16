import uuid

import pytest
from sqlmodel import Session, select

from domain.entities.webhook import Webhook
from domain.value_objects.webhook_event import EventType, OfferStatus
from domain.value_objects.webhook_type import WebhookType
from infrastructure.models.webhook import WebhookModel

pytestmark = pytest.mark.usefixtures("clean_db")

SOURCE_ID = "11111111-2222-3333-4444-555555555555"
REFERENCE = "2024-WEBHOOK-001"
WEBHOOK_TYPE = WebhookType.OFFER


# ---------------------------------------------------------------------------
# get_by_id
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_by_id_returns_webhook(webhook_repository):
    webhook = Webhook(
        source_id=SOURCE_ID,
        webhook_type=WEBHOOK_TYPE,
        event_type=EventType.CREE,
        reference=REFERENCE,
        payload={"event_type": str(EventType.CREE), "reference": REFERENCE},
    )
    await webhook_repository.insert(webhook)

    result = await webhook_repository.get_by_id(webhook.id)

    assert result == webhook


@pytest.mark.asyncio
async def test_get_by_id_raises_when_not_found(webhook_repository):
    with pytest.raises(ValueError, match=str(uuid.UUID(int=0))):
        await webhook_repository.get_by_id(uuid.UUID(int=0))


# ---------------------------------------------------------------------------
# Insert
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_insert_saves_webhook(webhook_repository):
    webhook = Webhook(
        source_id=SOURCE_ID,
        webhook_type=WEBHOOK_TYPE,
        event_type=EventType.CREE,
        reference=REFERENCE,
        payload={"event_type": str(EventType.CREE), "reference": REFERENCE},
    )

    await webhook_repository.insert(webhook)

    saved = await webhook_repository.get_by_id(webhook.id)
    assert saved.id == webhook.id
    assert saved.source_id == SOURCE_ID
    assert saved.event_type == EventType.CREE
    assert saved.reference == REFERENCE
    assert saved.status_id is None
    assert saved.payload == {"event_type": str(EventType.CREE), "reference": REFERENCE}


@pytest.mark.asyncio
async def test_insert_saves_status_id(webhook_repository):
    webhook = Webhook(
        source_id=SOURCE_ID,
        webhook_type=WEBHOOK_TYPE,
        event_type=EventType.STATUT_CHANGE,
        reference=REFERENCE,
        payload={"event_type": str(EventType.STATUT_CHANGE), "reference": REFERENCE},
        status_id=OfferStatus.DIFFUSE,
    )

    await webhook_repository.insert(webhook)

    saved = await webhook_repository.get_by_id(webhook.id)
    assert saved.status_id == OfferStatus.DIFFUSE
    assert saved.event_type == EventType.STATUT_CHANGE


@pytest.mark.asyncio
async def test_insert_sets_timestamps(webhook_repository, db_engine):
    webhook = Webhook(
        source_id=SOURCE_ID,
        webhook_type=WEBHOOK_TYPE,
        event_type=EventType.CREE,
        reference=REFERENCE,
        payload={"event_type": str(EventType.CREE), "reference": REFERENCE},
    )

    await webhook_repository.insert(webhook)

    with Session(db_engine) as session:
        model = session.get(WebhookModel, webhook.id)
    assert model.created_at is not None
    assert model.updated_at is not None


# ---------------------------------------------------------------------------
# Uniqueness
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_insert_allows_multiple_event_types_for_same_reference(
    webhook_repository, db_engine
):
    for event_type in (EventType.CREE, EventType.MIS_A_JOUR, EventType.SUPPRIME):
        await webhook_repository.insert(
            Webhook(
                source_id=SOURCE_ID,
                webhook_type=WEBHOOK_TYPE,
                event_type=event_type,
                reference=REFERENCE,
                payload={"event_type": str(event_type), "reference": REFERENCE},
            )
        )

    with Session(db_engine) as session:
        rows = session.exec(
            select(WebhookModel).where(
                WebhookModel.source_id == SOURCE_ID,
                WebhookModel.reference == REFERENCE,
            )
        ).all()
    assert len(rows) == 3


@pytest.mark.asyncio
async def test_insert_allows_same_reference_different_source_ids(webhook_repository):
    payload = {"event_type": str(EventType.CREE), "reference": REFERENCE}
    first = Webhook(
        source_id=SOURCE_ID,
        webhook_type=WEBHOOK_TYPE,
        event_type=EventType.CREE,
        reference=REFERENCE,
        payload=payload,
    )
    second = Webhook(
        source_id="other-source-id",
        webhook_type=WEBHOOK_TYPE,
        event_type=EventType.CREE,
        reference=REFERENCE,
        payload=payload,
    )

    await webhook_repository.insert(first)
    await webhook_repository.insert(second)

    result1 = await webhook_repository.get_by_id(first.id)
    result2 = await webhook_repository.get_by_id(second.id)
    assert result1.id != result2.id


@pytest.mark.asyncio
async def test_insert_allows_same_source_id_different_references(webhook_repository):
    first = Webhook(
        source_id=SOURCE_ID,
        webhook_type=WEBHOOK_TYPE,
        event_type=EventType.CREE,
        reference=REFERENCE,
        payload={"event_type": str(EventType.CREE), "reference": REFERENCE},
    )
    second = Webhook(
        source_id=SOURCE_ID,
        webhook_type=WEBHOOK_TYPE,
        event_type=EventType.CREE,
        reference="OTHER-REF",
        payload={"event_type": str(EventType.CREE), "reference": "OTHER-REF"},
    )

    await webhook_repository.insert(first)
    await webhook_repository.insert(second)

    result1 = await webhook_repository.get_by_id(first.id)
    result2 = await webhook_repository.get_by_id(second.id)
    assert result1.id != result2.id
