from unittest.mock import MagicMock

import pytest

from config.app_config import QdrantConfig
from config.logger_names import LoggerName
from infrastructure.di.shared import shared_container
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.repositories.shared.null_vector_repository import (
    NullVectorRepository,
)
from infrastructure.repositories.shared.qdrant_repository import QdrantRepository


@pytest.fixture(autouse=True)
def clear_null_vector_repository_cache():
    shared_container._null_vector_repository.cache_clear()
    yield
    shared_container._null_vector_repository.cache_clear()


def _vector_repository(url: str | None):
    container = SharedContainer()
    container.app_config.override(MagicMock(qdrant=QdrantConfig(url=url, api_key="")))
    container.logger_service.override(MagicMock())
    return container.vector_repository()


class TestVectorRepositorySelection:
    def test_uses_qdrant_when_url_is_configured(self):
        assert isinstance(_vector_repository("http://localhost:6333"), QdrantRepository)

    def test_uses_null_repository_when_url_is_empty(self):
        assert isinstance(_vector_repository(""), NullVectorRepository)

    def test_warns_only_once_when_vector_database_is_disabled(self, caplog):
        with caplog.at_level("WARNING", logger=LoggerName.WEB.value):
            _vector_repository("")
            _vector_repository("")
        assert len(caplog.records) == 1


class TestNullVectorRepository:
    def test_delete_succeeds_without_errors(self):
        result = NullVectorRepository().delete_vectorized_documents([])
        assert result == {"deleted": 0, "errors": []}

    def test_semantic_search_returns_no_results(self):
        assert NullVectorRepository().semantic_search([0.1, 0.2]) == []
