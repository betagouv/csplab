from datetime import date, datetime, timezone
from unittest.mock import MagicMock

import pytest
from dependency_injector import providers
from sqlmodel import Session, select

from application.use_cases.import_organismes import BATCH_SIZE, ImportOrganismesCommand
from domain.gateways.organisme_gateway import IOrganismeGateway
from domain.value_objects.organisme import OrganismeData, OrganismeImportResource
from infrastructure.di.container import Container
from infrastructure.models.raw_organisme import RawOrganismeModel
from infrastructure.raw_organisme_repository import RawOrganismeRepository

pytestmark = pytest.mark.usefixtures("clean_db")

REFERENTIEL = "FINESS"
RESOURCE = OrganismeImportResource(
    url="https://example.org/finess-structures-journalier-20260819.json.gz",
    millesime=date(2026, 8, 19),
)


def _fetch_all(db_engine, referentiel: str = REFERENTIEL) -> list[RawOrganismeModel]:
    with Session(db_engine) as session:
        return list(
            session.exec(
                select(RawOrganismeModel).where(
                    RawOrganismeModel.referentiel == referentiel
                )
            )
        )


def _organismes(count: int) -> list[OrganismeData]:
    return [
        OrganismeData(referentiel=REFERENTIEL, external_id=str(i), data={"i": i})
        for i in range(count)
    ]


@pytest.fixture
def mock_organisme_gateway() -> MagicMock:
    return MagicMock(spec=IOrganismeGateway)


@pytest.fixture
def repository_spy(db_engine) -> MagicMock:
    return MagicMock(wraps=RawOrganismeRepository(engine=db_engine))


@pytest.fixture
def container(db_engine, mock_organisme_gateway, repository_spy) -> Container:
    c = Container()
    c.db_engine.override(providers.Object(db_engine))
    c.organisme_gateway.override(providers.Object(mock_organisme_gateway))
    c.raw_organisme_repository.override(providers.Object(repository_spy))
    return c


@pytest.mark.asyncio
async def test_batches_of_exactly_batch_size_upsert_once(
    container, mock_organisme_gateway, repository_spy, db_engine
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter(
        _organismes(BATCH_SIZE)
    )

    result = await container.import_organismes_use_case().execute(
        ImportOrganismesCommand()
    )

    repository_spy.upsert_batch.assert_called_once()
    assert len(_fetch_all(db_engine)) == BATCH_SIZE
    assert result.total_imported == BATCH_SIZE


@pytest.mark.asyncio
async def test_flushes_remaining_items_below_batch_size(
    container, mock_organisme_gateway, repository_spy, db_engine
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter(_organismes(2))

    result = await container.import_organismes_use_case().execute(
        ImportOrganismesCommand()
    )

    repository_spy.upsert_batch.assert_called_once()
    assert len(_fetch_all(db_engine)) == 2
    assert result.total_imported == 2


@pytest.mark.asyncio
async def test_more_than_batch_size_calls_upsert_batch_twice(
    container, mock_organisme_gateway, repository_spy, db_engine
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter(
        _organismes(BATCH_SIZE + 3)
    )

    result = await container.import_organismes_use_case().execute(
        ImportOrganismesCommand()
    )

    assert repository_spy.upsert_batch.call_count == 2
    assert len(_fetch_all(db_engine)) == BATCH_SIZE + 3
    assert result.total_imported == BATCH_SIZE + 3


@pytest.mark.asyncio
async def test_raw_organisme_has_correct_fields(
    container, mock_organisme_gateway, db_engine
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter(
        [OrganismeData(referentiel=REFERENTIEL, external_id="123456789", data={"a": 1})]
    )

    result = await container.import_organismes_use_case().execute(
        ImportOrganismesCommand()
    )

    saved = _fetch_all(db_engine)
    assert len(saved) == 1
    assert saved[0].referentiel == REFERENTIEL
    assert saved[0].millesime == "2026-08-19"
    assert saved[0].external_id == "123456789"
    assert saved[0].data == {"a": 1}
    assert saved[0].loaded_at is not None
    assert result.referentiel == REFERENTIEL
    assert result.millesime == "2026-08-19"
    assert result.total_imported == 1


@pytest.mark.asyncio
async def test_stream_organismes_called_with_found_resource(
    container, mock_organisme_gateway
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter([])

    await container.import_organismes_use_case().execute(ImportOrganismesCommand())

    mock_organisme_gateway.stream_organismes.assert_called_once_with(RESOURCE)


@pytest.mark.asyncio
async def test_no_organismes_streamed_does_not_upsert(
    container, mock_organisme_gateway, repository_spy, db_engine
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter([])

    await container.import_organismes_use_case().execute(ImportOrganismesCommand())

    repository_spy.upsert_batch.assert_not_called()
    assert _fetch_all(db_engine) == []


@pytest.mark.asyncio
async def test_no_organismes_streamed_does_not_delete(
    container, mock_organisme_gateway, repository_spy
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter([])

    await container.import_organismes_use_case().execute(ImportOrganismesCommand())

    repository_spy.delete_missing.assert_not_called()


@pytest.mark.asyncio
async def test_deletes_organismes_missing_from_latest_import(
    container, mock_organisme_gateway, db_engine
):
    stale = RawOrganismeModel(
        referentiel=REFERENTIEL,
        millesime="2026-08-18",
        external_id="stale",
        loaded_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
    )
    with Session(db_engine) as session:
        session.add(stale)
        session.commit()

    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter(
        [OrganismeData(referentiel=REFERENTIEL, external_id="123456789", data={"a": 1})]
    )

    result = await container.import_organismes_use_case().execute(
        ImportOrganismesCommand()
    )

    remaining = {row.external_id for row in _fetch_all(db_engine)}
    assert remaining == {"123456789"}
    assert result.total_deleted == 1


@pytest.mark.asyncio
async def test_delete_missing_uses_the_run_loaded_at_watermark(
    container, mock_organisme_gateway, repository_spy
):
    mock_organisme_gateway.find_resource.return_value = RESOURCE
    mock_organisme_gateway.stream_organismes.return_value = iter(
        [OrganismeData(referentiel=REFERENTIEL, external_id="123456789", data={"a": 1})]
    )

    await container.import_organismes_use_case().execute(ImportOrganismesCommand())

    upserted_loaded_at = repository_spy.upsert_batch.call_args.args[0][0].loaded_at
    deleted_loaded_before = repository_spy.delete_missing.call_args.args[1]
    assert deleted_loaded_before == upserted_loaded_at
