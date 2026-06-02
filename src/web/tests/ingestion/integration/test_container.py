from unittest.mock import MagicMock

import pytest

from config.app_config import AppConfig
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService


@pytest.fixture
def container(db):
    shared_container = SharedContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    shared_container.app_config.override(app_config)
    shared_container.logger_service.override(logger_service)
    shared_container.vector_repository.override(MagicMock())
    shared_container.embedding_generator.override(MagicMock())

    c = IngestionContainer()
    c.app_config.override(app_config)
    c.logger_service.override(logger_service)
    c.shared_container.override(shared_container)
    return c


class TestIngestionContainerWiring:
    def test_all_usecases_resolve(self, container):
        container.archive_offer_by_reference_usecase()
        container.archive_offers_usecase()
        container.clean_documents_usecase()
        container.list_metiers_usecase()
        container.list_offers_usecase()
        container.list_sources_usecase()
        container.upsert_offers_usecase()
        container.vectorize_documents_usecase()
