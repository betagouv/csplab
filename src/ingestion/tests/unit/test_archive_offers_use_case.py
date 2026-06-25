from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest
from dependency_injector import providers

from application.use_cases.archive_offer import ArchiveOfferUseCase
from infrastructure.di.container import Container
from tests.factories.domain_factories import SourceFactory
from tests.factories.talentsoft_factories import TalentsoftOfferFactory

SOURCE_ID = UUID("11111111-2222-3333-4444-555555555555")
CLIENT_ID_FRONT = "front-client-id"


@pytest.fixture
def mock_web_offers_gateway() -> MagicMock:
    gateway = MagicMock()
    gateway.fetch_references = AsyncMock(return_value=[])
    return gateway


@pytest.fixture
def mock_sources_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_talentsoft_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_archive_offer_use_case() -> MagicMock:
    use_case = MagicMock(spec=ArchiveOfferUseCase)
    use_case.execute = AsyncMock()
    return use_case


@pytest.fixture
def container(
    mock_web_offers_gateway,
    mock_sources_repo,
    mock_talentsoft_repo,
    mock_archive_offer_use_case,
) -> Container:
    c = Container()
    c.offers_by_source_gateway.override(providers.Object(mock_web_offers_gateway))
    c.sources_repository.override(providers.Object(mock_sources_repo))
    c.talentsoft_client_repository.override(providers.Object(mock_talentsoft_repo))
    c.archive_offer_use_case.override(providers.Object(mock_archive_offer_use_case))
    return c


def _make_talentsoft_client(pages: list[tuple[list, bool]]) -> MagicMock:
    client = MagicMock()
    client.get_all = AsyncMock(side_effect=list(pages))
    return client


@pytest.mark.asyncio
async def test_raises_when_source_not_found(container, mock_sources_repo):
    mock_sources_repo.get_by_source_id.return_value = None

    with pytest.raises(ValueError, match=str(SOURCE_ID)):
        await container.archive_offers_use_case().execute(source_id=SOURCE_ID)


@pytest.mark.asyncio
async def test_raises_when_talentsoft_client_not_found(
    container, mock_sources_repo, mock_talentsoft_repo
):
    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    mock_talentsoft_repo.get.return_value = None

    with pytest.raises(ValueError, match=str(SOURCE_ID)):
        await container.archive_offers_use_case().execute(source_id=SOURCE_ID)

    mock_talentsoft_repo.get.assert_called_once_with(CLIENT_ID_FRONT)


@pytest.mark.asyncio
async def test_no_archive_when_all_web_offers_exist_in_talentsoft(
    container,
    mock_sources_repo,
    mock_talentsoft_repo,
    mock_web_offers_gateway,
    mock_archive_offer_use_case,
):
    offers = TalentsoftOfferFactory.batch(size=3)
    references = [o.reference for o in offers]
    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    mock_talentsoft_repo.get.return_value = _make_talentsoft_client([(offers, False)])
    mock_web_offers_gateway.fetch_references = AsyncMock(return_value=references)

    await container.archive_offers_use_case().execute(source_id=SOURCE_ID)

    mock_archive_offer_use_case.execute.assert_not_called()


@pytest.mark.asyncio
async def test_archives_offers_absent_from_talentsoft(
    container,
    mock_sources_repo,
    mock_talentsoft_repo,
    mock_web_offers_gateway,
    mock_archive_offer_use_case,
):
    talentsoft_offers = TalentsoftOfferFactory.batch(size=2)
    stale_reference = "2026-999999"
    web_references = [o.reference for o in talentsoft_offers] + [stale_reference]

    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    mock_talentsoft_repo.get.return_value = _make_talentsoft_client(
        [(talentsoft_offers, False)]
    )
    mock_web_offers_gateway.fetch_references = AsyncMock(return_value=web_references)

    await container.archive_offers_use_case().execute(source_id=SOURCE_ID)

    mock_archive_offer_use_case.execute.assert_called_once_with(
        reference=stale_reference, source_id=str(SOURCE_ID)
    )


@pytest.mark.asyncio
async def test_archives_all_web_offers_when_talentsoft_is_empty(
    container,
    mock_sources_repo,
    mock_talentsoft_repo,
    mock_web_offers_gateway,
    mock_archive_offer_use_case,
):
    web_references = ["2026-111111", "2026-222222"]
    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    mock_talentsoft_repo.get.return_value = _make_talentsoft_client([([], False)])
    mock_web_offers_gateway.fetch_references = AsyncMock(return_value=web_references)

    await container.archive_offers_use_case().execute(source_id=SOURCE_ID)

    assert mock_archive_offer_use_case.execute.call_count == 2
    archived = {
        call.kwargs["reference"]
        for call in mock_archive_offer_use_case.execute.call_args_list
    }
    assert archived == set(web_references)


@pytest.mark.asyncio
async def test_no_archive_when_both_sources_are_empty(
    container,
    mock_sources_repo,
    mock_talentsoft_repo,
    mock_web_offers_gateway,
    mock_archive_offer_use_case,
):
    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    mock_talentsoft_repo.get.return_value = _make_talentsoft_client([([], False)])
    mock_web_offers_gateway.fetch_references = AsyncMock(return_value=[])

    await container.archive_offers_use_case().execute(source_id=SOURCE_ID)

    mock_archive_offer_use_case.execute.assert_not_called()


@pytest.mark.asyncio
async def test_fetches_web_references_with_correct_source_id(
    container,
    mock_sources_repo,
    mock_talentsoft_repo,
    mock_web_offers_gateway,
):
    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    mock_talentsoft_repo.get.return_value = _make_talentsoft_client([([], False)])

    await container.archive_offers_use_case().execute(source_id=SOURCE_ID)

    mock_web_offers_gateway.fetch_references.assert_called_once_with(SOURCE_ID)


@pytest.mark.asyncio
async def test_talentsoft_pagination_fetches_all_pages(
    container,
    mock_sources_repo,
    mock_talentsoft_repo,
    mock_web_offers_gateway,
    mock_archive_offer_use_case,
):
    first_page = TalentsoftOfferFactory.batch(size=2)
    second_page = TalentsoftOfferFactory.batch(size=1)
    all_references = [o.reference for o in first_page + second_page]

    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    client = _make_talentsoft_client([(first_page, True), (second_page, False)])
    mock_talentsoft_repo.get.return_value = client
    mock_web_offers_gateway.fetch_references = AsyncMock(return_value=all_references)

    await container.archive_offers_use_case().execute(source_id=SOURCE_ID)

    assert client.get_all.call_count == 2
    mock_archive_offer_use_case.execute.assert_not_called()
