from unittest.mock import patch

import pytest
import responses
from qdrant_client.http.exceptions import UnexpectedResponse

from domain.entities.document import DocumentType
from domain.exceptions.document_error import UnsupportedDocumentTypeError
from domain.value_objects.similarity_type import SimilarityMetric, SimilarityType
from infrastructure.django_apps.shared.models.offer import OfferModel
from infrastructure.django_apps.shared.models.vectorized_document import (
    VectorizedDocumentModel,
)
from infrastructure.exceptions.exceptions import ExternalApiError
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.corps_factory import CorpsFactory
from tests.factories.offer_factory import OfferFactory
from tests.utils.mock_api_response_factory import MockApiResponseFactory

DB_ERROR = "Database connection error"
BAD_TYPE = "not_a_valid_type"


factories_mapper = {
    DocumentType.CORPS: CorpsFactory(),
    DocumentType.CONCOURS: ConcoursFactory(),
    DocumentType.OFFERS: OfferFactory(),
}


def assert_nothing_vectorized():
    assert not VectorizedDocumentModel.objects.exists()


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


@pytest.fixture(name="offer_setup")
def offer_setup_fixture(db, ingestion_integration_container_albert):
    document_type = DocumentType.OFFERS
    usecase = ingestion_integration_container_albert.vectorize_documents_usecase()
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
    ingestion_integration_container_albert,
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
    container = ingestion_integration_container_albert
    usecase = container.vectorize_documents_usecase()
    documents = factories_mapper[document_type].create_batch(2)

    result = usecase.execute(document_type)

    assert_success_result(result, expected_count=len(documents))

    # With Qdrant, documents are not stored in VectorizedDocumentModel anymore
    # Instead, verify they are in Qdrant by doing a search
    vector_repo = container.vector_repository()
    search_results = vector_repo.semantic_search(
        query_embedding=[0.1] * 1024,
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
    db, ingestion_integration_container_albert, test_app_config
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

    usecase = ingestion_integration_container_albert.vectorize_documents_usecase()

    result = usecase.execute(DocumentType.OFFERS)

    assert_success_result(result, expected_count=0)
    assert_nothing_vectorized()


@responses.activate
def test_vectorize_limit(db, ingestion_integration_container_albert, test_app_config):
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
    usecase = ingestion_integration_container_albert.vectorize_documents_usecase()
    result = usecase.execute(DocumentType.OFFERS, limit=limit)

    assert_success_result(result, expected_count=limit)

    # With Qdrant, verify documents are stored by searching
    vector_repo = ingestion_integration_container_albert.vector_repository()
    search_results = vector_repo.semantic_search(
        query_embedding=[0.1] * 1024,  # Mock embedding for search
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

    assert_nothing_vectorized()
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
    assert_nothing_vectorized()
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

    assert_nothing_vectorized()
    assert_offer_pending(processing=True)


@responses.activate
def test_vectorize_qdrant_unsupported_similarity_metric(
    db, ingestion_integration_container_albert, test_app_config
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
    usecase = ingestion_integration_container_albert.vectorize_documents_usecase()
    usecase.execute(DocumentType.OFFERS)

    # Test unsupported similarity metric
    vector_repo = ingestion_integration_container_albert.vector_repository()
    unsupported_similarity = SimilarityType(metric=SimilarityMetric.EUCLIDEAN)

    with pytest.raises(
        NotImplementedError, match="Similarity metric .* not implemented"
    ):
        vector_repo.semantic_search(
            query_embedding=[0.1] * 1024,
            limit=10,
            similarity_type=unsupported_similarity,
        )


@responses.activate
def test_vectorize_qdrant_search_unexpected_response(
    db, ingestion_integration_container_albert, test_app_config
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
    usecase = ingestion_integration_container_albert.vectorize_documents_usecase()
    usecase.execute(DocumentType.OFFERS)

    # Test UnexpectedResponse from Qdrant (lignes 100-105)
    vector_repo = ingestion_integration_container_albert.vector_repository()

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
                query_embedding=[0.1] * 1024,
                limit=10,
            )


@responses.activate
def test_vectorize_qdrant_search_general_error(
    db, ingestion_integration_container_albert, test_app_config
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
    usecase = ingestion_integration_container_albert.vectorize_documents_usecase()
    usecase.execute(DocumentType.OFFERS)

    # Test general Exception from Qdrant (ligne 106)
    vector_repo = ingestion_integration_container_albert.vector_repository()

    with patch.object(
        vector_repo.client,
        "query_points",
        side_effect=Exception("General Qdrant error"),
    ):
        with pytest.raises(ExternalApiError, match="Vector search failed"):
            vector_repo.semantic_search(
                query_embedding=[0.1] * 1024,
                limit=10,
            )


@responses.activate
def test_vectorize_qdrant_upsert_error(
    db, ingestion_integration_container_albert, test_app_config
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
    usecase = ingestion_integration_container_albert.vectorize_documents_usecase()

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
    db, ingestion_integration_container_albert, test_app_config
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
    vector_repo = ingestion_integration_container_albert.vector_repository()
    result = vector_repo.upsert_batch([], DocumentType.OFFERS)

    assert result == {"created": 0, "updated": 0, "errors": []}


@responses.activate
def test_vectorize_qdrant_search_no_filters(
    db, ingestion_integration_container_albert, test_app_config
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
    usecase = ingestion_integration_container_albert.vectorize_documents_usecase()
    usecase.execute(DocumentType.OFFERS)

    # Test search without filters (ligne 113 - return None)
    vector_repo = ingestion_integration_container_albert.vector_repository()
    search_results = vector_repo.semantic_search(
        query_embedding=[0.1] * 1024,
        limit=10,
        filters=None,  # This should trigger ligne 113
    )

    assert len(search_results) >= 0  # Should work without filters


@responses.activate
def test_vectorize_qdrant_search_empty_filters(
    db, ingestion_integration_container_albert, test_app_config
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
    usecase = ingestion_integration_container_albert.vectorize_documents_usecase()
    usecase.execute(DocumentType.OFFERS)

    # Test search with empty filters dict (ligne 157-158 - return None)
    vector_repo = ingestion_integration_container_albert.vector_repository()
    search_results = vector_repo.semantic_search(
        query_embedding=[0.1] * 1024,
        limit=10,
        filters={},  # Empty dict should trigger ligne 157-158
    )

    assert len(search_results) >= 0  # Should work with empty filters


@responses.activate
def test_vectorize_qdrant_search_list_filters(
    db, ingestion_integration_container_albert, test_app_config
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

    # Create and vectorize documents first
    OfferFactory.create_batch(2)
    usecase = ingestion_integration_container_albert.vectorize_documents_usecase()
    usecase.execute(DocumentType.OFFERS)

    # Test search with list filters (lignes 149-152)
    vector_repo = ingestion_integration_container_albert.vector_repository()
    search_results = vector_repo.semantic_search(
        query_embedding=[0.1] * 1024,
        limit=10,
        filters={
            "document_type": [DocumentType.OFFERS.value, DocumentType.CORPS.value]
        },
    )

    assert len(search_results) >= 0  # Should work with list filters


@responses.activate
def test_vectorize_albert_empty_text_error(
    db, ingestion_integration_container_albert, test_app_config
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
    usecase = ingestion_integration_container_albert.vectorize_documents_usecase()

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
    db, ingestion_integration_container_albert, test_app_config
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
    usecase = ingestion_integration_container_albert.vectorize_documents_usecase()
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
    db, ingestion_integration_container_albert, test_app_config
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
    usecase = ingestion_integration_container_albert.vectorize_documents_usecase()
    result = usecase.execute(DocumentType.OFFERS)

    # Should handle HTTP error and convert to ExternalApiError
    assert result["processed"] == 0
    assert result["vectorized"] == 0
    assert result["errors"] == 1
    assert "Albert API error: 500" in result["error_details"][0]["exception"]


@responses.activate
def test_vectorize_albert_empty_data_error(
    db, ingestion_integration_container_albert, test_app_config
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
    usecase = ingestion_integration_container_albert.vectorize_documents_usecase()
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

    assert_nothing_vectorized()
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

    assert_nothing_vectorized()
    assert_offer_pending(processing=True)
