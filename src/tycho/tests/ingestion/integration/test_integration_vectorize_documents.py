from unittest.mock import patch

import pytest
import responses
from django.conf import settings
from qdrant_client.http.exceptions import UnexpectedResponse

from config.app_config import AppConfig
from domain.entities.document import DocumentType
from domain.exceptions.document_error import UnsupportedDocumentTypeError
from domain.value_objects.similarity_type import SimilarityMetric, SimilarityType
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.django_apps.shared.models.offer import OfferModel
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.albert_embedding_generator import (
    AlbertEmbeddingGenerator,
)
from infrastructure.gateways.shared.http_client import SyncHttpClient
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.postgres_concours_repository import (
    PostgresConcoursRepository,
)
from infrastructure.repositories.shared.postgres_corps_repository import (
    PostgresCorpsRepository,
)
from infrastructure.repositories.shared.postgres_metier_repository import (
    PostgresMetierRepository,
)
from infrastructure.repositories.shared.postgres_offers_repository import (
    PostgresOffersRepository,
)
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.corps_factory import CorpsFactory
from tests.factories.offer_factory import OfferFactory
from tests.fixtures.shared_fixtures import create_shared_qdrant_repository
from tests.utils.mock_api_response_factory import MockApiResponseFactory

DB_ERROR = "Database connection error"
BAD_TYPE = "not_a_valid_type"
TWO_DOCUMENTS = 2
THREE_DOCUMENTS = 3


factories_mapper = {
    DocumentType.CORPS: CorpsFactory(),
    DocumentType.CONCOURS: ConcoursFactory(),
    DocumentType.OFFERS: OfferFactory(),
}


def assert_offer_pending(processing: bool):
    assert OfferModel.objects.filter(
        processed_at__isnull=True, processing=processing
    ).exists()


def assert_success_result(result, *, expected_count):
    assert result["processed"] == expected_count
    assert result["vectorized"] == expected_count
    assert result["errors"] == 0
    assert result["error_details"] == []


def assert_error_result(result, *, expected_exception_message):
    assert result["processed"] == 0
    assert result["vectorized"] == 0
    assert result["errors"] == 1
    assert len(result["error_details"]) == 1
    assert result["error_details"][0]["exception"] == expected_exception_message


@pytest.fixture
def vectorize_integration_container(db):

    container = IngestionContainer()

    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()

    container.logger_service.override(logger_service)
    container.app_config.override(app_config)
    container.shared_container.app_config.override(app_config)

    http_client = SyncHttpClient()
    albert_embedding_generator = AlbertEmbeddingGenerator(
        config=app_config.albert, http_client=http_client
    )
    container.shared_container.embedding_generator.override(albert_embedding_generator)

    postgres_corps_repo = PostgresCorpsRepository(logger_service)
    container.shared_container.corps_repository.override(postgres_corps_repo)

    postgres_concours_repo = PostgresConcoursRepository(logger_service)
    container.shared_container.concours_repository.override(postgres_concours_repo)

    postgres_offers_repo = PostgresOffersRepository(logger_service)
    container.shared_container.offers_repository.override(postgres_offers_repo)

    postgres_metier_repo = PostgresMetierRepository(logger_service)
    container.shared_container.metiers_repository.override(postgres_metier_repo)

    qdrant_repository = create_shared_qdrant_repository()
    container.shared_container.vector_repository.override(qdrant_repository)

    return container


@pytest.fixture(name="offer_setup")
def offer_setup_fixture(db, vectorize_integration_container):
    document_type = DocumentType.OFFERS
    usecase = vectorize_integration_container.vectorize_documents_usecase()
    repository = usecase.repository_factory.get_repository(document_type)
    factories_mapper[document_type].create()
    return usecase, repository, document_type


@responses.activate
@pytest.mark.parametrize(
    "document_type", [DocumentType.CORPS, DocumentType.CONCOURS, DocumentType.OFFERS]
)
def test_vectorize_entity_integration(
    db,
    document_type,
    vectorize_integration_container,
    test_app_config,
):
    # Mock Albert API with responses
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    # Use Albert container directly
    container = vectorize_integration_container
    usecase = container.vectorize_documents_usecase()
    documents = factories_mapper[document_type].create_batch(2)

    result = usecase.execute(document_type)

    assert_success_result(result, expected_count=len(documents))

    # With Qdrant, documents are not stored in VectorizedDocumentModel anymore
    # Instead, verify they are in Qdrant by doing a search
    vector_repo = container.vector_repository()
    search_results = vector_repo.semantic_search(
        query_embedding=[0.1]
        * settings.EMBEDDING_DIMENSION,  # Mock embedding for search
        limit=10,
        filters={"document_type": document_type.value},
    )

    assert len(search_results) == len(documents)
    for result in search_results:
        assert result.document.document_type == document_type
        assert result.document.content is not None
        assert result.document.metadata is not None
        assert round(result.score, 1) >= 0.0


@responses.activate
def test_vectorize_empty_list_integration(
    db, vectorize_integration_container, test_app_config
):
    # Mock Albert API with responses
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    usecase = vectorize_integration_container.vectorize_documents_usecase()

    result = usecase.execute(DocumentType.OFFERS)

    assert_success_result(result, expected_count=0)


@responses.activate
def test_vectorize_limit(db, vectorize_integration_container, test_app_config):
    # Mock Albert API with responses
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    limit = 2
    OfferFactory.create_batch(limit + 1)
    usecase = vectorize_integration_container.vectorize_documents_usecase()
    result = usecase.execute(DocumentType.OFFERS, limit=limit)

    assert_success_result(result, expected_count=limit)

    # With Qdrant, verify documents are stored by searching
    vector_repo = vectorize_integration_container.vector_repository()
    search_results = vector_repo.semantic_search(
        query_embedding=[0.1]
        * settings.EMBEDDING_DIMENSION,  # Mock embedding for search
        limit=10,
        filters={"document_type": DocumentType.OFFERS.value},
    )
    assert len(search_results) == limit

    assert OfferModel.objects.filter(processed_at__isnull=False).count() == limit


@responses.activate
def test_vectorize_get_pending_processing_error(offer_setup, test_app_config):
    # Mock Albert API with responses
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    usecase, repository, document_type = offer_setup

    with patch.object(
        repository,
        "get_pending_processing",
        side_effect=Exception(DB_ERROR),
    ) as mocked_method:
        with pytest.raises(Exception, match=DB_ERROR):
            usecase.execute(document_type)
        mocked_method.assert_called_once()

    assert_offer_pending(processing=False)


@responses.activate
def test_vectorize_vectorize_single_source_error(offer_setup, test_app_config):
    # Mock Albert API with responses
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    usecase, _, document_type = offer_setup

    with patch.object(
        usecase,
        "vectorize_single_source",
        side_effect=UnsupportedDocumentTypeError(BAD_TYPE),
    ) as mocked_method:
        result = usecase.execute(document_type)
        mocked_method.assert_called_once()

    assert_error_result(
        result,
        expected_exception_message=f"Document type: {BAD_TYPE} is not supported yet",
    )
    assert_offer_pending(processing=False)


@responses.activate
def test_vectorize_upsert_batch_error(offer_setup, test_app_config):
    # Mock Albert API with responses
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    usecase, _, document_type = offer_setup

    with patch.object(
        usecase.vector_repository,
        "upsert_batch",
        side_effect=Exception(DB_ERROR),
    ) as mocked_method:
        with pytest.raises(Exception, match=DB_ERROR):
            usecase.execute(document_type)
        mocked_method.assert_called_once()

    assert_offer_pending(processing=True)


@responses.activate
def test_vectorize_qdrant_unsupported_similarity_metric(
    db, vectorize_integration_container, test_app_config
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

    # Create and vectorize a document first
    OfferFactory.create()
    usecase = vectorize_integration_container.vectorize_documents_usecase()
    usecase.execute(DocumentType.OFFERS)

    # Test unsupported similarity metric
    vector_repo = vectorize_integration_container.vector_repository()
    unsupported_similarity = SimilarityType(metric=SimilarityMetric.EUCLIDEAN)

    with pytest.raises(
        NotImplementedError, match="Similarity metric .* not implemented"
    ):
        vector_repo.semantic_search(
            query_embedding=[0.1] * settings.EMBEDDING_DIMENSION,
            limit=10,
            similarity_type=unsupported_similarity,
        )


@responses.activate
def test_vectorize_qdrant_search_unexpected_response(
    db, vectorize_integration_container, test_app_config
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

    # Create and vectorize a document first
    OfferFactory.create()
    usecase = vectorize_integration_container.vectorize_documents_usecase()
    usecase.execute(DocumentType.OFFERS)

    # Test UnexpectedResponse from Qdrant (lignes 100-105)
    vector_repo = vectorize_integration_container.vector_repository()

    # Create a proper UnexpectedResponse with required parameters
    qdrant_error = UnexpectedResponse(
        status_code=500,
        reason_phrase="Internal Server Error",
        content=b"Qdrant server error",
        headers={},
    )

    with patch.object(
        vector_repo.client,
        "query_points",
        side_effect=qdrant_error,
    ):
        with pytest.raises(ExternalApiError, match="Vector search failed"):
            vector_repo.semantic_search(
                query_embedding=[0.1] * settings.EMBEDDING_DIMENSION,
                limit=10,
            )


@responses.activate
def test_vectorize_qdrant_search_general_error(
    db, vectorize_integration_container, test_app_config
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

    # Create and vectorize a document first
    OfferFactory.create()
    usecase = vectorize_integration_container.vectorize_documents_usecase()
    usecase.execute(DocumentType.OFFERS)

    # Test general Exception from Qdrant (ligne 106)
    vector_repo = vectorize_integration_container.vector_repository()

    with patch.object(
        vector_repo.client,
        "query_points",
        side_effect=Exception("General Qdrant error"),
    ):
        with pytest.raises(ExternalApiError, match="Vector search failed"):
            vector_repo.semantic_search(
                query_embedding=[0.1] * settings.EMBEDDING_DIMENSION,
                limit=10,
            )


@responses.activate
def test_vectorize_qdrant_upsert_error(
    db, vectorize_integration_container, test_app_config
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

    # Create a document to vectorize
    OfferFactory.create()
    usecase = vectorize_integration_container.vectorize_documents_usecase()

    # Test Exception from Qdrant upsert (lignes 143-145)
    with patch.object(
        usecase.vector_repository.client,
        "upsert",
        side_effect=Exception("Qdrant upsert error"),
    ):
        with pytest.raises(ExternalApiError, match="Qdrant upsert error"):
            usecase.execute(DocumentType.OFFERS)


@responses.activate
def test_vectorize_qdrant_empty_documents_upsert(
    db, vectorize_integration_container, test_app_config
):
    # Mock Albert API (won't be called)
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    # Test empty documents list (ligne 108)
    vector_repo = vectorize_integration_container.vector_repository()
    result = vector_repo.upsert_batch([], DocumentType.OFFERS)

    assert result == {"created": 0, "updated": 0, "errors": []}


@responses.activate
def test_vectorize_qdrant_search_no_filters(
    db, vectorize_integration_container, test_app_config
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

    OfferFactory.create()
    usecase = vectorize_integration_container.vectorize_documents_usecase()
    usecase.execute(DocumentType.OFFERS)

    vector_repo = vectorize_integration_container.vector_repository()
    search_results = vector_repo.semantic_search(
        query_embedding=[0.1] * settings.EMBEDDING_DIMENSION,
        limit=10,
        filters=None,
    )

    assert len(search_results) == 1


@responses.activate
def test_vectorize_albert_empty_text_error(
    db, vectorize_integration_container, test_app_config
):
    # Mock Albert API (won't be called due to empty text)
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    OfferFactory.create()
    usecase = vectorize_integration_container.vectorize_documents_usecase()

    with patch.object(
        usecase.text_extractor,
        "extract_content",
        return_value="   ",
    ):
        result = usecase.execute(DocumentType.OFFERS)

    assert result["processed"] == 0
    assert result["vectorized"] == 0
    assert result["errors"] == 1
    assert "Text content cannot be empty" in result["error_details"][0]["exception"]


@responses.activate
def test_vectorize_albert_invalid_response_error(
    db, vectorize_integration_container, test_app_config
):
    # Mock Albert API with invalid response structure
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    invalid_response = {"invalid": "structure"}  # Missing required fields
    responses.add(
        responses.POST,
        albert_url,
        json=invalid_response,
        status=200,
        content_type="application/json",
    )

    OfferFactory.create()
    usecase = vectorize_integration_container.vectorize_documents_usecase()
    result = usecase.execute(DocumentType.OFFERS)

    # Should handle ValidationError and convert to ExternalApiError
    assert result["processed"] == 0
    assert result["vectorized"] == 0
    assert result["errors"] == 1
    assert (
        "Invalid Albert API response structure"
        in result["error_details"][0]["exception"]
    )


@responses.activate
def test_vectorize_albert_http_error(
    db, vectorize_integration_container, test_app_config
):
    # Mock Albert API with HTTP error
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    responses.add(
        responses.POST,
        albert_url,
        json={"error": "Internal server error"},
        status=500,
        content_type="application/json",
    )

    OfferFactory.create()
    usecase = vectorize_integration_container.vectorize_documents_usecase()
    result = usecase.execute(DocumentType.OFFERS)

    # Should handle HTTP error and convert to ExternalApiError
    assert result["processed"] == 0
    assert result["vectorized"] == 0
    assert result["errors"] == 1
    assert "Albert API error: 500" in result["error_details"][0]["exception"]


@responses.activate
def test_vectorize_albert_empty_data_error(
    db, vectorize_integration_container, test_app_config
):
    # Mock Albert API with empty data using factory
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    empty_data_response = (
        MockApiResponseFactory.create_albert_embedding_response_empty_data()
    )
    responses.add(
        responses.POST,
        albert_url,
        json=empty_data_response,
        status=200,
        content_type="application/json",
    )

    OfferFactory.create()
    usecase = vectorize_integration_container.vectorize_documents_usecase()
    result = usecase.execute(DocumentType.OFFERS)

    # Should handle empty data and raise ExternalApiError
    assert result["processed"] == 0
    assert result["vectorized"] == 0
    assert result["errors"] == 1
    error_message = result["error_details"][0]["exception"]
    assert (
        "No embedding data in Albert API response" in error_message
        or "Albert API error" in error_message
    )


@responses.activate
def test_vectorize_mark_as_processed_error(offer_setup, test_app_config):
    # Mock Albert API with responses
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    usecase, repository, document_type = offer_setup

    with patch.object(
        repository,
        "mark_as_processed",
        side_effect=Exception(DB_ERROR),
    ) as mocked_method:
        with pytest.raises(Exception, match=DB_ERROR):
            usecase.execute(document_type)
        mocked_method.assert_called_once()

    assert_offer_pending(processing=True)


@responses.activate
def test_vectorize_mark_as_pending_error(offer_setup, test_app_config):
    albert_url = f"{test_app_config.albert.api_base_url}v1/embeddings"
    mock_response = MockApiResponseFactory.create_albert_embedding_response()
    responses.add(
        responses.POST,
        albert_url,
        json=mock_response,
        status=200,
        content_type="application/json",
    )

    usecase, repository, document_type = offer_setup

    with (
        patch.object(
            usecase,
            "vectorize_single_source",
            side_effect=UnsupportedDocumentTypeError(BAD_TYPE),
        ) as mocked_vectorize,
        patch.object(
            repository,
            "mark_as_pending",
            side_effect=Exception(DB_ERROR),
        ) as mocked_mark,
    ):
        with pytest.raises(Exception, match=DB_ERROR):
            usecase.execute(document_type)
        mocked_vectorize.assert_called_once()
        mocked_mark.assert_called_once()

    assert_offer_pending(processing=True)
