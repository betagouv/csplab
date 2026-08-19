from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest
from dependency_injector import providers

from application.use_cases.import_organismes import BATCH_SIZE
from domain.gateways.organisme_gateway import IOrganismeGateway
from domain.repositories.raw_organisme_repository import IRawOrganismeRepository
from domain.value_objects.organisme import OrganismeData, OrganismeImportResource
from infrastructure.di.container import Container

RESOURCE = OrganismeImportResource(
    url="https://example.org/finess-structures-journalier-20260819.json.gz",
    millesime=date(2026, 8, 19),
)


@pytest.fixture
def mock_organisme_gateway() -> MagicMock:
    return MagicMock(spec=IOrganismeGateway)


@pytest.fixture
def mock_raw_organisme_repo() -> MagicMock:
    repo = MagicMock(spec=IRawOrganismeRepository)
    repo.upsert_batch = AsyncMock()
    repo.delete_missing = AsyncMock(return_value=0)
    return repo


@pytest.fixture
def container(mock_organisme_gateway, mock_raw_organisme_repo) -> Container:
    c = Container()
    c.organisme_gateway.override(providers.Object(mock_organisme_gateway))
    c.raw_organisme_repository.override(providers.Object(mock_raw_organisme_repo))
    return c


def _organismes(count: int) -> list[OrganismeData]:
    return [
        OrganismeData(referentiel="FINESS", external_id=str(i), data={"i": i})
        for i in range(count)
    ]


@pytest.mark.asyncio
async def test_batches_of_exactly_batch_size_upsert_once(
    container, mock_organisme_gateway, mock_raw_organisme_repo
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter(
        _organismes(BATCH_SIZE)
    )

    await container.import_organismes_use_case().execute()

    mock_raw_organisme_repo.upsert_batch.assert_called_once()
    batch = mock_raw_organisme_repo.upsert_batch.call_args.args[0]
    assert len(batch) == BATCH_SIZE


@pytest.mark.asyncio
async def test_flushes_remaining_items_below_batch_size(
    container, mock_organisme_gateway, mock_raw_organisme_repo
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter(_organismes(2))

    await container.import_organismes_use_case().execute()

    mock_raw_organisme_repo.upsert_batch.assert_called_once()
    batch = mock_raw_organisme_repo.upsert_batch.call_args.args[0]
    assert len(batch) == 2


@pytest.mark.asyncio
async def test_more_than_batch_size_calls_upsert_batch_twice(
    container, mock_organisme_gateway, mock_raw_organisme_repo
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter(
        _organismes(BATCH_SIZE + 3)
    )

    await container.import_organismes_use_case().execute()

    assert mock_raw_organisme_repo.upsert_batch.call_count == 2
    first_batch = mock_raw_organisme_repo.upsert_batch.call_args_list[0].args[0]
    second_batch = mock_raw_organisme_repo.upsert_batch.call_args_list[1].args[0]
    assert len(first_batch) == BATCH_SIZE
    assert len(second_batch) == 3


@pytest.mark.asyncio
async def test_raw_organisme_has_correct_fields(
    container, mock_organisme_gateway, mock_raw_organisme_repo
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter(
        [OrganismeData(referentiel="FINESS", external_id="123456789", data={"a": 1})]
    )

    await container.import_organismes_use_case().execute()

    batch = mock_raw_organisme_repo.upsert_batch.call_args.args[0]
    saved = batch[0]
    assert saved.referentiel == "FINESS"
    assert saved.millesime == "2026-08-19"
    assert saved.external_id == "123456789"
    assert saved.data == {"a": 1}
    assert saved.loaded_at is not None


@pytest.mark.asyncio
async def test_stream_organismes_called_with_found_resource(
    container, mock_organisme_gateway, mock_raw_organisme_repo
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter([])

    await container.import_organismes_use_case().execute()

    mock_organisme_gateway.stream_organismes.assert_called_once_with(RESOURCE)


@pytest.mark.asyncio
async def test_no_organismes_streamed_does_not_upsert(
    container, mock_organisme_gateway, mock_raw_organisme_repo
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter([])

    await container.import_organismes_use_case().execute()

    mock_raw_organisme_repo.upsert_batch.assert_not_called()


@pytest.mark.asyncio
async def test_no_organismes_streamed_does_not_delete(
    container, mock_organisme_gateway, mock_raw_organisme_repo
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter([])

    await container.import_organismes_use_case().execute()

    mock_raw_organisme_repo.delete_missing.assert_not_called()


@pytest.mark.asyncio
async def test_deletes_missing_organismes_for_streamed_referentiel(
    container, mock_organisme_gateway, mock_raw_organisme_repo
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter(
        [OrganismeData(referentiel="FINESS", external_id="123456789", data={"a": 1})]
    )

    await container.import_organismes_use_case().execute()

    mock_raw_organisme_repo.delete_missing.assert_called_once()
    args = mock_raw_organisme_repo.delete_missing.call_args.args
    assert args[0] == "FINESS"


@pytest.mark.asyncio
async def test_delete_missing_uses_the_run_loaded_at_watermark(
    container, mock_organisme_gateway, mock_raw_organisme_repo
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter(
        [OrganismeData(referentiel="FINESS", external_id="123456789", data={"a": 1})]
    )

    await container.import_organismes_use_case().execute()

    upserted_loaded_at = mock_raw_organisme_repo.upsert_batch.call_args.args[0][
        0
    ].loaded_at
    deleted_loaded_before = mock_raw_organisme_repo.delete_missing.call_args.args[1]
    assert deleted_loaded_before == upserted_loaded_at
