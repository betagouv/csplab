from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest
from dependency_injector import providers

from domain.repositories.webhook_repository import IWebhookRepository
from domain.value_objects.webhook_event import EventType, WebhookActionType
from domain.value_objects.webhook_type import WebhookType
from infrastructure.di.container import Container
from tests.factories.domain_factories import SourceFactory
from tests.factories.talentsoft_factories import TalentsoftOfferFactory

SOURCE_ID = UUID("11111111-2222-3333-4444-555555555555")
CLIENT_ID_FRONT = "front-client-id"


@pytest.fixture
def mock_webhook_repo() -> MagicMock:
    repo = MagicMock(spec=IWebhookRepository)
    repo.insert = AsyncMock()
    return repo


@pytest.fixture
def mock_dispatch() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_sources_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_talentsoft_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def container(
    mock_sources_repo,
    mock_talentsoft_repo,
    mock_webhook_repo,
    mock_dispatch,
) -> Container:
    c = Container()
    c.sources_repository.override(providers.Object(mock_sources_repo))
    c.talentsoft_client_repository.override(providers.Object(mock_talentsoft_repo))
    c.webhook_repository.override(providers.Object(mock_webhook_repo))
    c.dispatch_save_raw_offer_webhook.override(providers.Object(mock_dispatch))
    return c


def _make_client(pages: list[tuple[list, bool]]) -> MagicMock:
    client = MagicMock()
    client.get_all = AsyncMock(side_effect=list(pages))
    return client


@pytest.mark.asyncio
async def test_raises_when_source_not_found(container, mock_sources_repo):
    mock_sources_repo.get_by_source_id.return_value = None

    with pytest.raises(ValueError, match=str(SOURCE_ID)):
        await container.import_offers_use_case().execute(source_id=SOURCE_ID)


@pytest.mark.asyncio
async def test_raises_when_talentsoft_client_not_found(
    container, mock_sources_repo, mock_talentsoft_repo
):
    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    mock_talentsoft_repo.get.return_value = None

    with pytest.raises(ValueError, match=str(SOURCE_ID)):
        await container.import_offers_use_case().execute(source_id=SOURCE_ID)

    mock_talentsoft_repo.get.assert_called_once_with(CLIENT_ID_FRONT)


@pytest.mark.asyncio
async def test_single_page_inserts_webhooks_and_dispatches(
    container, mock_sources_repo, mock_talentsoft_repo, mock_webhook_repo, mock_dispatch
):
    offers = TalentsoftOfferFactory.batch(size=3)
    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    mock_talentsoft_repo.get.return_value = _make_client([(offers, False)])

    await container.import_offers_use_case().execute(source_id=SOURCE_ID)

    assert mock_webhook_repo.insert.call_count == 3
    assert mock_dispatch.call_count == 3


@pytest.mark.asyncio
async def test_webhooks_have_cree_event_type_and_correct_fields(
    container, mock_sources_repo, mock_talentsoft_repo, mock_webhook_repo
):
    offers = TalentsoftOfferFactory.batch(size=2)
    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    mock_talentsoft_repo.get.return_value = _make_client([(offers, False)])

    await container.import_offers_use_case().execute(source_id=SOURCE_ID)

    inserted = [call.args[0] for call in mock_webhook_repo.insert.call_args_list]
    references = {o.reference for o in offers}

    for webhook in inserted:
        assert webhook.event_type == EventType.CREE
        assert webhook.webhook_type == WebhookType.OFFER
        assert webhook.source_id == str(SOURCE_ID)
        assert webhook.status_id is None
        assert webhook.action_type == WebhookActionType.SAVE_RAW_OFFER
        assert webhook.reference in references


@pytest.mark.asyncio
async def test_dispatch_receives_webhook_id(
    container, mock_sources_repo, mock_talentsoft_repo, mock_webhook_repo, mock_dispatch
):
    offers = TalentsoftOfferFactory.batch(size=1)
    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    mock_talentsoft_repo.get.return_value = _make_client([(offers, False)])

    await container.import_offers_use_case().execute(source_id=SOURCE_ID)

    inserted_webhook = mock_webhook_repo.insert.call_args.args[0]
    mock_dispatch.assert_called_once_with(str(inserted_webhook.id))


@pytest.mark.asyncio
async def test_multiple_pages_processes_all_offers(
    container, mock_sources_repo, mock_talentsoft_repo, mock_webhook_repo, mock_dispatch
):
    first_page = TalentsoftOfferFactory.batch(size=2)
    second_page = TalentsoftOfferFactory.batch(size=1)
    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    client = _make_client([(first_page, True), (second_page, False)])
    mock_talentsoft_repo.get.return_value = client

    await container.import_offers_use_case().execute(source_id=SOURCE_ID)

    assert mock_webhook_repo.insert.call_count == 3
    assert mock_dispatch.call_count == 3
    assert client.get_all.call_count == 2


@pytest.mark.asyncio
async def test_pagination_increments_page_number(
    container, mock_sources_repo, mock_talentsoft_repo, mock_webhook_repo
):
    offers = TalentsoftOfferFactory.batch(size=1)
    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    client = _make_client([(offers, True), ([], False)])
    mock_talentsoft_repo.get.return_value = client

    await container.import_offers_use_case().execute(source_id=SOURCE_ID)

    first_call = client.get_all.call_args_list[0]
    second_call = client.get_all.call_args_list[1]
    assert first_call.kwargs["start"] == 1
    assert second_call.kwargs["start"] == 2


@pytest.mark.asyncio
async def test_empty_page_does_not_insert_or_dispatch(
    container, mock_sources_repo, mock_talentsoft_repo, mock_webhook_repo, mock_dispatch
):
    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    mock_talentsoft_repo.get.return_value = _make_client([([], False)])

    await container.import_offers_use_case().execute(source_id=SOURCE_ID)

    mock_webhook_repo.insert.assert_not_called()
    mock_dispatch.assert_not_called()
