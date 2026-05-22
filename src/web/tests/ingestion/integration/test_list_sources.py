import pytest

from config.app_config import AppConfig
from domain.value_objects.source_type import SourceType
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.source_factory import SourceFactory


@pytest.fixture(name="ingestion_container")
def ingestion_container_fixture(db):
    container = IngestionContainer()
    shared_container = SharedContainer()

    app_config = AppConfig.from_django_settings()
    shared_container.app_config.override(app_config)

    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    container.shared_container.override(shared_container)
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


def test_returns_empty_list_when_no_sources(ingestion_container):
    result = ingestion_container.list_sources_usecase().execute()

    assert result == []


def test_returns_all_sources(ingestion_container):
    SourceFactory.create_model()
    SourceFactory.create_model()

    result = ingestion_container.list_sources_usecase().execute()

    assert len(result) == 2  # noqa: PLR2004


def test_returns_correct_source_entity_fields(ingestion_container):
    model = SourceFactory.create_model(
        source_type=SourceType.TALENTSOFT,
        client_id_front="my_front_id",
        client_id_back="my_back_id",
        base_url_front="https://front.talentsoft.com",
        base_url_back="https://back.talentsoft.com",
    )

    result = ingestion_container.list_sources_usecase().execute()

    assert len(result) == 1
    source = result[0]
    assert source.id == model.id
    assert source.source_id == model.source_id
    assert source.type == SourceType.TALENTSOFT
    assert source.client_id_front == "my_front_id"
    assert source.client_id_back == "my_back_id"
    assert source.base_url_front == "https://front.talentsoft.com"
    assert source.base_url_back == "https://back.talentsoft.com"
