from unittest.mock import AsyncMock, MagicMock

import pytest
from dependency_injector import providers

from application.usecases.prepare_talentsoft_organisations import (
    PrepareTalentsoftOrganisationsCommand,
)
from infrastructure.di.container import Container
from infrastructure.exceptions.exceptions import ExternalApiError
from tests.conftest import SOURCE_UUID
from tests.conftest import TALENTSOFT_FRONT_CLIENT_ID as CLIENT_ID_FRONT
from tests.factories.domain_factories import SourceFactory
from tests.factories.talentsoft_factories import (
    TalentsoftCodedObjectFactory,
    TalentsoftOrganisationFactory,
)


@pytest.fixture
def mock_sources_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_talentsoft_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def container(mock_sources_repo, mock_talentsoft_repo) -> Container:
    c = Container()
    c.sources_repository.override(providers.Object(mock_sources_repo))
    c.talentsoft_client_repository.override(providers.Object(mock_talentsoft_repo))
    return c


def _make_client(referentiel: list, details: list) -> MagicMock:
    client = MagicMock()
    client.get_organisations_referentiel = AsyncMock(return_value=referentiel)
    client.get_organisation_detail = AsyncMock(side_effect=details)
    return client


@pytest.mark.asyncio
async def test_raises_when_source_not_found(container, mock_sources_repo):
    mock_sources_repo.get_by_source_id.return_value = None

    with pytest.raises(ValueError, match=str(SOURCE_UUID)):
        await container.prepare_talentsoft_organisations_usecase().execute(
            PrepareTalentsoftOrganisationsCommand(source_id=SOURCE_UUID)
        )


@pytest.mark.asyncio
async def test_merges_referentiel_and_detail_into_payloads(
    container, mock_sources_repo, mock_talentsoft_repo
):
    referentiel = TalentsoftCodedObjectFactory.batch(
        size=2, type="organisation", hasChildren=False
    )
    details = [TalentsoftOrganisationFactory.build() for _ in referentiel]
    source = SourceFactory.build(source_id=SOURCE_UUID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    client = _make_client(referentiel, details)
    mock_talentsoft_repo.get.return_value = client

    batches = await container.prepare_talentsoft_organisations_usecase().execute(
        PrepareTalentsoftOrganisationsCommand(source_id=SOURCE_UUID)
    )

    assert len(batches) == 1
    payloads = batches[0]
    assert len(payloads) == 2
    assert {p.code for p in payloads} == {item.code for item in referentiel}
    assert client.get_organisation_detail.call_count == 2


@pytest.mark.asyncio
async def test_splits_into_batches_of_100(
    container, mock_sources_repo, mock_talentsoft_repo
):
    referentiel = TalentsoftCodedObjectFactory.batch(size=150, type="organisation")
    details = [TalentsoftOrganisationFactory.build() for _ in referentiel]
    source = SourceFactory.build(source_id=SOURCE_UUID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    mock_talentsoft_repo.get.return_value = _make_client(referentiel, details)

    batches = await container.prepare_talentsoft_organisations_usecase().execute(
        PrepareTalentsoftOrganisationsCommand(source_id=SOURCE_UUID)
    )

    assert [len(batch) for batch in batches] == [100, 50]


@pytest.mark.asyncio
async def test_skips_organisation_when_detail_fetch_fails(
    container, mock_sources_repo, mock_talentsoft_repo
):
    referentiel = TalentsoftCodedObjectFactory.batch(size=2, type="organisation")
    details = [
        ExternalApiError("boom", api_name="Talentsoft Front API"),
        TalentsoftOrganisationFactory.build(),
    ]
    source = SourceFactory.build(source_id=SOURCE_UUID, client_id_front=CLIENT_ID_FRONT)
    mock_sources_repo.get_by_source_id.return_value = source
    mock_talentsoft_repo.get.return_value = _make_client(referentiel, details)

    batches = await container.prepare_talentsoft_organisations_usecase().execute(
        PrepareTalentsoftOrganisationsCommand(source_id=SOURCE_UUID)
    )

    assert len(batches) == 1
    assert len(batches[0]) == 1
    assert batches[0][0].code == referentiel[1].code
