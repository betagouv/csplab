from unittest.mock import AsyncMock, MagicMock

import pytest

from application.use_cases.save_webhook import SaveWebhookUseCase
from domain.repositories.webhook_repository import IWebhookRepository
from domain.value_objects.webhook_event import EventType, OfferStatus, WebhookEvent
from domain.value_objects.webhook_type import WebhookType
from tests.factories.domain_factories import SourceFactory

PAYLOAD = {"event_type": "vacancy_new", "reference": "REF-001"}
WEBHOOK_TYPE = WebhookType.OFFER


@pytest.mark.asyncio
async def test_execute_inserts_webhook():
    mock_repo = MagicMock(spec=IWebhookRepository)
    mock_repo.insert = AsyncMock()
    source = SourceFactory.build(source_id="source-1")

    use_case = SaveWebhookUseCase(repository=mock_repo)
    event = WebhookEvent(event_type=EventType.CREE, reference="REF-001")

    await use_case.execute(
        event=event, source=source, payload=PAYLOAD, webhook_type=WEBHOOK_TYPE
    )

    mock_repo.insert.assert_called_once()
    inserted = mock_repo.insert.call_args[0][0]
    assert inserted.source_id == "source-1"
    assert inserted.webhook_type == WEBHOOK_TYPE
    assert inserted.event_type == EventType.CREE
    assert inserted.reference == "REF-001"
    assert inserted.status_id is None
    assert inserted.payload == PAYLOAD


@pytest.mark.asyncio
async def test_execute_maps_status_id():
    mock_repo = MagicMock(spec=IWebhookRepository)
    mock_repo.insert = AsyncMock()
    source = SourceFactory.build(source_id="source-1")

    use_case = SaveWebhookUseCase(repository=mock_repo)
    event = WebhookEvent(
        event_type=EventType.STATUT_CHANGE,
        reference="REF-002",
        status=OfferStatus.DIFFUSE,
    )

    await use_case.execute(
        event=event,
        source=source,
        payload={
            "event_type": "vacancy_status",
            "reference": "REF-002",
            "statusId": "Diffuse",
        },
        webhook_type=WEBHOOK_TYPE,
    )

    inserted = mock_repo.insert.call_args[0][0]
    assert inserted.status_id == OfferStatus.DIFFUSE
    assert inserted.event_type == EventType.STATUT_CHANGE


@pytest.mark.asyncio
async def test_execute_stores_payload_as_received():
    mock_repo = MagicMock(spec=IWebhookRepository)
    mock_repo.insert = AsyncMock()
    source = SourceFactory.build()
    payload = {"event_type": "vacancy_new", "reference": "REF-003", "extra": "data"}

    use_case = SaveWebhookUseCase(repository=mock_repo)
    event = WebhookEvent(event_type=EventType.CREE, reference="REF-003")

    await use_case.execute(
        event=event, source=source, payload=payload, webhook_type=WEBHOOK_TYPE
    )

    inserted = mock_repo.insert.call_args[0][0]
    assert inserted.payload == payload


@pytest.mark.asyncio
async def test_execute_raises_when_repository_fails():
    mock_repo = MagicMock(spec=IWebhookRepository)
    mock_repo.insert = AsyncMock(side_effect=Exception("DB error"))
    source = SourceFactory.build()

    use_case = SaveWebhookUseCase(repository=mock_repo)
    event = WebhookEvent(event_type=EventType.CREE, reference="REF-001")

    with pytest.raises(Exception, match="DB error"):
        await use_case.execute(
            event=event, source=source, payload=PAYLOAD, webhook_type=WEBHOOK_TYPE
        )
