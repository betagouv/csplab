import pytest
import responses
from faker import Faker

from config.app_config import AppConfig
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
from infrastructure.external_gateways.albert_embedding_generator import (
    AlbertEmbeddingGenerator,
)
from infrastructure.gateways.shared.http_client import SyncHttpClient
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.postgres_corps_repository import (
    PostgresCorpsRepository,
)
from tests.fixtures.shared_fixtures import create_shared_qdrant_repository
from tests.utils.mock_api_response_factory import MockApiResponseFactory

fake = Faker()

# Test constants
EXPECTED_TEST_CORPS_COUNT = 2
EXPECTED_TEST_CORPS_COUNT_WITH_LIMIT = 1
PORT = 6333


@pytest.fixture(name="test_app_config")
def test_app_config_fixture():
    return AppConfig.from_django_settings()


@pytest.fixture(name="shared_container")
def shared_container_fixture(test_app_config):
    container = SharedContainer()

    container.app_config.override(test_app_config)

    logger_service = LoggerService()
    container.logger_service.override(logger_service)

    postgres_corps_repository = PostgresCorpsRepository(logger_service)
    container.corps_repository.override(postgres_corps_repository)

    # Use shared Qdrant repository fixture
    shared_qdrant_repository = create_shared_qdrant_repository()
    container.vector_repository.override(shared_qdrant_repository)

    return container


@pytest.fixture(name="candidate_container")
def candidate_container_fixture(shared_container, test_app_config):
    container = CandidateContainer()
    container.shared_container.override(shared_container)

    http_client = SyncHttpClient()
    mock_embedding_generator = AlbertEmbeddingGenerator(
        config=test_app_config.albert, http_client=http_client
    )
    shared_container.embedding_generator.override(mock_embedding_generator)

    logger_service = LoggerService()
    container.logger_service.override(logger_service)

    return container


@pytest.fixture(name="retrieve_corps_usecase")
def retrieve_corps_usecase_fixture(candidate_container):
    return candidate_container.retrieve_corps_usecase()


@pytest.fixture(name="corps_data")
def corps_data_fixture(shared_container, test_app_config):
    corps_repository = shared_container.corps_repository()
    vector_repository = shared_container.vector_repository()

    # Get mock embeddings for test data
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    embeddings = mock_response["data"][0]["embedding"]

    # Create test corps data
    corps_list = []
    for i in range(EXPECTED_TEST_CORPS_COUNT):
        corps = Corps(
            code=f"CODE{i + 1}",
            category=Category.A,
            ministry=Ministry.MAA,
            diploma=Diploma(5),
            access_modalities=[AccessModality.CONCOURS_EXTERNE],
            label=Label(
                short_value=f"Corps {i + 1}",
                value=f"Corps de test {i + 1}",
            ),
        )
        corps_list.append(corps)

    result = corps_repository.upsert_batch(corps_list)
    if result["errors"]:
        raise Exception(f"Failed to save Corps entities: {result['errors']}")

    # Create vectorized documents for each corps
    vectorized_documents = []
    for corps in corps_list:
        vectorized_documents.append(
            VectorizedDocument(
                entity_id=corps.id,
                document_type=DocumentType.CORPS,
                content=corps.label.value,
                embedding=embeddings,  # Use the mock embedding
                metadata={"document_type": "CORPS"},
            )
        )
    vector_repository.upsert_batch(vectorized_documents, DocumentType.CORPS)

    return corps_list


@responses.activate
def test_retrieve_corps_with_valid_query_returns_results(
    db, retrieve_corps_usecase, corps_data, test_app_config
):
    # Mock Albert API
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    query = corps_data[0].label.value

    result = retrieve_corps_usecase.execute(query, limit=10)

    assert len(result) == EXPECTED_TEST_CORPS_COUNT
    assert isinstance(result, list)
    assert isinstance(result[0], tuple)
    assert isinstance(result[0][0], Corps)
    assert isinstance(result[0][1], float)

    # Verify that the queried corps is in the results (order may vary with same scores)
    returned_labels = {corps.label.value for corps, score in result}
    assert query in returned_labels

    # Verify scores are valid (cosine similarity can be negative)
    for _, score in result:
        assert -1.0 <= round(score, 1) <= 1.0

    returned_ids = {corps.id for corps, score in result}
    expected_ids = {corps.id for corps in corps_data}
    assert returned_ids == expected_ids


def test_retrieve_corps_with_empty_query_returns_empty_list(
    db,
    retrieve_corps_usecase,
    corps_data,
):
    result = retrieve_corps_usecase.execute("", limit=10)

    assert result == []


@responses.activate
def test_retrieve_corps_with_no_matching_documents_returns_empty_list(
    db,
    retrieve_corps_usecase,
    test_app_config,
):
    # Mock Albert API
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    result = retrieve_corps_usecase.execute("some random query", limit=10)

    assert result == []


@responses.activate
def test_retrieve_corps_respects_limit_parameter(
    db, retrieve_corps_usecase, corps_data, test_app_config
):
    # Mock Albert API
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    query = corps_data[0].label.value

    result = retrieve_corps_usecase.execute(query, limit=1)

    assert len(result) == EXPECTED_TEST_CORPS_COUNT_WITH_LIMIT
    assert isinstance(result[0], tuple)
    assert isinstance(result[0][0], Corps)
    assert isinstance(result[0][1], float)
