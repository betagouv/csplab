"""Shared fixtures for ingestion tests."""

import pytest

from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.pgvector_repository import PgVectorRepository
from infrastructure.repositories.shared.postgres_concours_repository import (
    PostgresConcoursRepository,
)
from infrastructure.repositories.shared.postgres_corps_repository import (
    PostgresCorpsRepository,
)
from infrastructure.repositories.shared.postgres_offers_repository import (
    PostgresOffersRepository,
)
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.in_memory_concours_repository import InMemoryConcoursRepository
from tests.utils.in_memory_corps_repository import InMemoryCorpsRepository
from tests.utils.in_memory_document_repository import InMemoryDocumentRepository
from tests.utils.in_memory_offers_repository import InMemoryOffersRepository
from tests.utils.in_memory_vector_repository import InMemoryVectorRepository
from tests.utils.mock_embedding_generator import MockEmbeddingGenerator


def _create_ingestion_container(in_memory: bool = True):
    """Factory function to create ingestion containers with specified configuration."""
    container = IngestionContainer()

    logger_service = LoggerService()
    container.logger_service.override(logger_service)

    embedding_fixtures = load_fixture("embedding_fixtures.json")
    mock_embedding_generator = MockEmbeddingGenerator(embedding_fixtures)
    container.shared_container.embedding_generator.override(mock_embedding_generator)

    if in_memory:
        # Use in-memory repositories for unit tests
        in_memory_corps_repo = InMemoryCorpsRepository()
        container.shared_container.corps_repository.override(in_memory_corps_repo)

        in_memory_concours_repo = InMemoryConcoursRepository()
        container.shared_container.concours_repository.override(in_memory_concours_repo)

        in_memory_offers_repo = InMemoryOffersRepository()
        container.shared_container.offers_repository.override(in_memory_offers_repo)

        in_memory_document_repo = InMemoryDocumentRepository()
        container.document_persister.override(in_memory_document_repo)

        in_memory_vector_repo = InMemoryVectorRepository()
        container.vector_repository.override(in_memory_vector_repo)
    else:
        # Use Django persistence for integration tests
        postgres_corps_repo = PostgresCorpsRepository()
        container.shared_container.corps_repository.override(postgres_corps_repo)

        postgres_concours_repo = PostgresConcoursRepository()
        container.shared_container.concours_repository.override(postgres_concours_repo)

        postgres_offers_repo = PostgresOffersRepository()
        container.shared_container.offers_repository.override(postgres_offers_repo)

        pgvector_repo = PgVectorRepository()
        container.vector_repository.override(pgvector_repo)

    return container


@pytest.fixture(name="ingestion_container")
def ingestion_container_fixture():
    """Set up ingestion container with in-memory repositories for unit tests."""
    return _create_ingestion_container(in_memory=True)


@pytest.fixture(name="ingestion_integration_container")
def ingestion_integration_container_fixture():
    """Set up ingestion container with Django persistence for integration tests."""
    return _create_ingestion_container(in_memory=False)
