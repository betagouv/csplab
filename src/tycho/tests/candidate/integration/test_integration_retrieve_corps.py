"""Integration tests for RetrieveCorpsUsecase with external adapters."""

from datetime import datetime, timezone

import pytest
from pydantic import HttpUrl

from domain.entities.corps import Corps
from domain.entities.document import DocumentType
from domain.entities.vectorized_document import VectorizedDocument
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.diploma import Diploma
from domain.value_objects.label import Label
from domain.value_objects.ministry import Ministry
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.external_gateways.configs.openai_config import (
    OpenAIConfig,
    OpenAIGatewayConfig,
)
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared import pgvector_repository as pgvector_repo
from infrastructure.repositories.shared import (
    postgres_corps_repository as postgres_corps_repo,
)
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.mock_embedding_generator import MockEmbeddingGenerator

# Test constants
EXPECTED_TEST_CORPS_COUNT = 2
EXPECTED_TEST_CORPS_COUNT_WITH_LIMIT = 1


@pytest.fixture(name="embeddings", scope="session")
def embeddings_fixture():
    """Load fixtures all at once."""
    return load_fixture("embedding_fixtures.json")


@pytest.fixture(name="shared_container")
def shared_container_fixture():
    """Set up shared container."""
    container = SharedContainer()

    openai_gateway_config = OpenAIGatewayConfig(
        openai_config=OpenAIConfig(
            api_key="fake-api-key",
            base_url=HttpUrl("https://api.openai.com/v1"),
            model="text-embedding-3-large",
        )
    )
    container.config.override(openai_gateway_config)

    logger_service = LoggerService()
    container.logger_service.override(logger_service)

    postgres_corps_repository = postgres_corps_repo.PostgresCorpsRepository(
        logger_service
    )
    container.corps_repository.override(postgres_corps_repository)

    pgvector_repository = pgvector_repo.PgVectorRepository()
    container.vector_repository.override(pgvector_repository)

    return container


@pytest.fixture(name="candidate_container")
def candidate_container_fixture(shared_container, embeddings):
    """Set up candidate container."""
    container = CandidateContainer()
    container.shared_container.override(shared_container)

    mock_embedding_generator = MockEmbeddingGenerator(embeddings)
    shared_container.embedding_generator.override(mock_embedding_generator)

    logger_service = LoggerService()
    container.logger_service.override(logger_service)

    return container


@pytest.fixture(name="retrieve_corps_usecase")
def retrieve_corps_usecase_fixture(candidate_container):
    """Retrieve Corps usecase."""
    return candidate_container.retrieve_corps_usecase()


@pytest.fixture(name="corps_data")
def corps_data_fixture(shared_container, embeddings):
    """Create Corps and vectorized documents in database."""
    corps_repository = shared_container.corps_repository()
    vector_repository = shared_container.vector_repository()

    corps_list = []
    for corps_id, fixture_data in list(embeddings.items())[:EXPECTED_TEST_CORPS_COUNT]:
        corps = Corps(
            code=f"CODE{corps_id}",
            category=Category.A,
            ministry=Ministry.MAA,
            diploma=Diploma(5),
            access_modalities=[AccessModality.CONCOURS_EXTERNE],
            label=Label(
                short_value=fixture_data["long_label"][:20],
                value=fixture_data["long_label"],
            ),
        )
        corps_list.append(corps)

    result = corps_repository.upsert_batch(corps_list)
    if result["errors"]:
        raise Exception(f"Failed to save Corps entities: {result['errors']}")

    # Create a mapping from corps to fixture data based on order
    fixture_items = list(embeddings.items())[:EXPECTED_TEST_CORPS_COUNT]

    for i, corps in enumerate(corps_list):
        _, fixture_data = fixture_items[i]
        vectorized_doc = VectorizedDocument(
            entity_id=corps.id,
            document_type=DocumentType.CORPS,
            content=fixture_data["long_label"],
            embedding=fixture_data["embedding"],
            metadata={"document_type": "CORPS"},
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        vector_repository.store_embedding(vectorized_doc)

    return corps_list


def test_retrieve_corps_with_valid_query_returns_results(
    db, retrieve_corps_usecase, corps_data, embeddings
):
    """Test retrieving Corps with scores using real database."""
    query = list(embeddings.values())[0]["long_label"]

    result = retrieve_corps_usecase.execute(query, limit=10)

    assert len(result) == EXPECTED_TEST_CORPS_COUNT
    assert isinstance(result, list)
    assert isinstance(result[0], tuple)
    assert isinstance(result[0][0], Corps)
    assert isinstance(result[0][1], float)

    assert result[0][0].label.value == query

    # Verify scores are between 0 and 1 (relevance scores)
    for _, score in result:
        assert 0.0 <= score <= 1.0

    returned_ids = {corps.id for corps, score in result}
    expected_ids = {corps.id for corps in corps_data}
    assert returned_ids == expected_ids


def test_retrieve_corps_with_empty_query_returns_empty_list(
    db, retrieve_corps_usecase, corps_data
):
    """Test that empty query returns empty list with real database."""
    result = retrieve_corps_usecase.execute("", limit=10)

    assert result == []


def test_retrieve_corps_with_no_matching_documents_returns_empty_list(
    db,
    retrieve_corps_usecase,
):
    """Test query with no matching vectorized documents returns empty list."""
    result = retrieve_corps_usecase.execute("some random query", limit=10)

    assert result == []


def test_retrieve_corps_respects_limit_parameter(
    db, retrieve_corps_usecase, corps_data, embeddings
):
    """Test that limit parameter is respected."""
    query = list(embeddings.values())[0]["long_label"]

    result = retrieve_corps_usecase.execute(query, limit=1)

    assert len(result) == EXPECTED_TEST_CORPS_COUNT_WITH_LIMIT
    assert isinstance(result[0], tuple)
    assert isinstance(result[0][0], Corps)
    assert isinstance(result[0][1], float)
