"""Shared fixtures for ingestion tests."""

from datetime import datetime

import pytest
from faker import Faker
from pydantic import HttpUrl

from domain.entities.document import Document, DocumentType
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.external_gateways.configs.openai_config import (
    OpenAIConfig,
    OpenAIGatewayConfig,
)
from infrastructure.external_gateways.configs.piste_config import (
    PisteConfig,
    PisteGatewayConfig,
)
from infrastructure.gateways.ingestion import load_documents_strategy_factory
from infrastructure.gateways.shared.http_client import SyncHttpClient
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.ingestion.postgres_document_repository import (
    PostgresDocumentRepository,
)
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

fake = Faker()

# DATAS


@pytest.fixture(scope="session", name="raw_corps_documents")
def raw_corps_documents_fixture():
    """Load fixture data once for all tests."""
    return load_fixture("corps_ingres_20251117.json")


@pytest.fixture(name="corps_document")
def corps_document_fixture():
    """Create a single corps document for testing."""
    return Document(
        id=None,
        external_id="test_corps_doc",
        raw_data={"name": "Test Document"},
        type=DocumentType.CORPS,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture(name="corps_documents")
def corps_documents_fixture():
    """Create multiple corps documents for batch testing."""
    return [
        Document(
            id=None,
            external_id="corps_1",
            raw_data={"name": "Corps 1", "description": "First corps"},
            type=DocumentType.CORPS,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        Document(
            id=None,
            external_id="corps_2",
            raw_data={"name": "Corps 2", "description": "Second corps"},
            type=DocumentType.CORPS,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]


@pytest.fixture(name="concours_documents")
def concours_documents_fixture():
    """Create sample concours documents."""
    return [
        Document(
            id=None,
            external_id="exam_1",
            raw_data={"name": "Exam 1"},
            type=DocumentType.CONCOURS,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]


# CONFIGS


@pytest.fixture(name="piste_gateway_config")
def piste_gateway_config_fixture():
    """Setup piste gateway config for usecase and tests."""
    return PisteGatewayConfig(
        piste_config=PisteConfig(
            oauth_base_url=HttpUrl(fake.url()),
            ingres_base_url=HttpUrl(fake.url()),
            client_id=fake.uuid4(),
            client_secret=fake.word(),
        )
    )


@pytest.fixture(name="openai_gateway_config")
def openai_gateway_config_fixture():
    """Setup openai gateway config for testing usecase."""
    return OpenAIGatewayConfig(
        openai_config=OpenAIConfig(
            api_key=fake.uuid4(),
            base_url=HttpUrl(fake.url()),
            model=fake.word(),
        )
    )


# CONTAINERS


def _create_ingestion_container(
    piste_gateway_config: PisteGatewayConfig,
    openai_gateway_config: OpenAIGatewayConfig,
    in_memory: bool = True,
):
    """Factory function to create ingestion containers with specified configuration."""
    container = IngestionContainer()

    logger_service = LoggerService()
    container.logger_service.override(logger_service)

    embedding_fixtures = load_fixture("embedding_fixtures.json")
    mock_embedding_generator = MockEmbeddingGenerator(embedding_fixtures)
    container.shared_container.embedding_generator.override(mock_embedding_generator)

    if in_memory:
        # Use in-memory repositories for unit tests
        in_memory_document_repo = InMemoryDocumentRepository()
        container.document_persister.override(in_memory_document_repo)

        in_memory_corps_repo = InMemoryCorpsRepository()
        container.shared_container.corps_repository.override(in_memory_corps_repo)

        in_memory_concours_repo = InMemoryConcoursRepository()
        container.shared_container.concours_repository.override(in_memory_concours_repo)

        in_memory_offers_repo = InMemoryOffersRepository()
        container.shared_container.offers_repository.override(in_memory_offers_repo)

        in_memory_vector_repo = InMemoryVectorRepository()
        container.vector_repository.override(in_memory_vector_repo)
    else:
        # Use Django persistence for integration tests
        postgres_document_repo = PostgresDocumentRepository()
        container.document_persister.override(postgres_document_repo)

        postgres_corps_repo = PostgresCorpsRepository()
        container.shared_container.corps_repository.override(postgres_corps_repo)

        postgres_concours_repo = PostgresConcoursRepository()
        container.shared_container.concours_repository.override(postgres_concours_repo)

        postgres_offers_repo = PostgresOffersRepository()
        container.shared_container.offers_repository.override(postgres_offers_repo)

        pgvector_repo = PgVectorRepository()
        container.vector_repository.override(pgvector_repo)

        container.config.override(piste_gateway_config)
        container.shared_container.config.override(openai_gateway_config)

        http_client = SyncHttpClient()
        container.http_client.override(http_client)

    return container


@pytest.fixture(name="ingestion_container")
def ingestion_container_fixture(piste_gateway_config, openai_gateway_config):
    """Set up ingestion container with in-memory repositories for unit tests."""
    return _create_ingestion_container(
        piste_gateway_config, openai_gateway_config, in_memory=True
    )


@pytest.fixture(name="documents_ingestion_container")
def documents_ingestion_container_fixture(ingestion_container):
    """Set up documents ingestion container for unit tests."""
    # Override with in-memory repository for unit tests
    in_memory_document_repo = InMemoryDocumentRepository()
    ingestion_container.document_repository.override(in_memory_document_repo)

    # Create real factory with the same in-memory repository as document_fetcher
    test_factory = load_documents_strategy_factory.LoadDocumentsStrategyFactory(
        document_fetcher=in_memory_document_repo
    )
    ingestion_container.load_documents_strategy_factory.override(test_factory)

    return ingestion_container


@pytest.fixture(name="ingestion_integration_container")
def ingestion_integration_container_fixture(
    piste_gateway_config, openai_gateway_config
):
    """Set up ingestion container with Django persistence for integration tests."""
    return _create_ingestion_container(
        piste_gateway_config, openai_gateway_config, in_memory=False
    )


# REPOSITORIES


@pytest.fixture(name="documents_repository")
def documents_repository_fixture(documents_ingestion_container):
    """Get the document documents_repository from the documents_ingestion_container."""
    return documents_ingestion_container.document_repository()


# USECASES


@pytest.fixture(name="documents_usecase")
def documents_usecase_fixture(documents_ingestion_container):
    """Create the load documents documents_usecase."""
    return documents_ingestion_container.load_documents_usecase()


@pytest.fixture(name="documents_integration_usecase")
def documents_integration_usecase_fixture(
    ingestion_integration_container,
):
    """Set up container dependencies for Corps LoadDocuments integration tests."""
    return ingestion_integration_container.load_documents_usecase()
