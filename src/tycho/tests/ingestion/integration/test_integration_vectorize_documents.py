from typing import Any, Dict
from unittest.mock import patch

import pytest
from django.conf import settings
from httpx import Headers
from qdrant_client.http.exceptions import UnexpectedResponse

from config.app_config import AppConfig
from domain.entities.document import DocumentType
from domain.exceptions.document_error import UnsupportedDocumentTypeError
from domain.value_objects.similarity_type import SimilarityMetric, SimilarityType
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.django_apps.shared.models.offer import OfferModel
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.gateways.shared.logger import LoggerService
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


def mock_embedding_response(
    httpx_mock,
    config,
    embedding_response: Dict[str, Any] | None = None,
    status_code: int = 200,
):
    if not embedding_response:
        embedding_response = MockApiResponseFactory.create_albert_embedding_response()

    httpx_mock.add_response(
        method="POST",
        url=f"{config.albert.api_base_url}v1/embeddings",
        json=embedding_response,
        status_code=status_code,
        is_reusable=True,
    )


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
def vectorize_integration_container():
    shared_qdrant_repository = create_shared_qdrant_repository()

    container = IngestionContainer()

    # Setup shared container with real repositories (except embedding generator)
    shared_container = SharedContainer()

    app_config = AppConfig.from_django_settings()
    shared_container.app_config.override(app_config)

    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    shared_container.vector_repository.override(shared_qdrant_repository)

    container.shared_container.override(shared_container)

    container.app_config.override(app_config)
    container.logger_service.override(logger_service)

    return container


@pytest.fixture(name="offer_setup")
def offer_setup_fixture(vectorize_integration_container):
    document_type = DocumentType.OFFERS
    usecase = vectorize_integration_container.vectorize_documents_usecase()
    repository = usecase.repository_factory.get_repository(document_type)
    factories_mapper[document_type].create()
    return usecase, repository, document_type


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
@pytest.mark.parametrize(
    "document_type", [DocumentType.CORPS, DocumentType.CONCOURS, DocumentType.OFFERS]
)
def test_vectorize_entity_integration(
    db,
    document_type,
    vectorize_integration_container,
    httpx_mock,
):
    test_app_config = vectorize_integration_container.app_config()
    mock_embedding_response(httpx_mock, test_app_config)

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


def test_vectorize_empty_list_integration(db, vectorize_integration_container):

    usecase = vectorize_integration_container.vectorize_documents_usecase()

    result = usecase.execute(DocumentType.OFFERS)

    assert_success_result(result, expected_count=0)


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
def test_vectorize_limit(db, vectorize_integration_container, httpx_mock):
    test_app_config = vectorize_integration_container.app_config()
    mock_embedding_response(httpx_mock, test_app_config)

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


def test_vectorize_get_pending_processing_error(
    db,
    offer_setup,
):
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


def test_vectorize_vectorize_single_source_error(db, offer_setup):

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


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
def test_vectorize_upsert_batch_error(
    db, offer_setup, vectorize_integration_container, httpx_mock
):
    test_app_config = vectorize_integration_container.app_config()
    mock_embedding_response(httpx_mock, test_app_config)

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


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
def test_vectorize_qdrant_unsupported_similarity_metric(
    db, vectorize_integration_container, httpx_mock
):
    test_app_config = vectorize_integration_container.app_config()
    mock_embedding_response(httpx_mock, test_app_config)

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


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
def test_vectorize_qdrant_search_unexpected_response(
    db, vectorize_integration_container, httpx_mock
):
    test_app_config = vectorize_integration_container.app_config()
    mock_embedding_response(httpx_mock, test_app_config)

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
        headers=Headers(),
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


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
def test_vectorize_qdrant_search_general_error(
    db, vectorize_integration_container, httpx_mock
):
    test_app_config = vectorize_integration_container.app_config()
    mock_embedding_response(httpx_mock, test_app_config)

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


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
def test_vectorize_qdrant_upsert_error(db, vectorize_integration_container, httpx_mock):
    test_app_config = vectorize_integration_container.app_config()
    mock_embedding_response(httpx_mock, test_app_config)

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


def test_vectorize_qdrant_empty_documents_upsert(db, vectorize_integration_container):
    # Test empty documents list (ligne 108)
    vector_repo = vectorize_integration_container.vector_repository()
    result = vector_repo.upsert_batch([], DocumentType.OFFERS)

    assert result == {"created": 0, "updated": 0, "errors": []}


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
def test_vectorize_qdrant_search_no_filters(
    db, vectorize_integration_container, httpx_mock
):
    test_app_config = vectorize_integration_container.app_config()
    mock_embedding_response(httpx_mock, test_app_config)

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


def test_vectorize_albert_empty_text_error(db, vectorize_integration_container):

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


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
def test_vectorize_albert_invalid_response_error(
    db, vectorize_integration_container, httpx_mock
):
    test_app_config = vectorize_integration_container.app_config()

    # Mock Albert API with invalid response structure
    invalid_response = {"invalid": "structure"}  # Missing required fields
    mock_embedding_response(httpx_mock, test_app_config, invalid_response)

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


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
def test_vectorize_albert_http_error(db, vectorize_integration_container, httpx_mock):

    test_app_config = vectorize_integration_container.app_config()
    # Mock Albert API with HTTP 500 error
    mock_embedding_response(httpx_mock, test_app_config, status_code=500)

    OfferFactory.create()
    usecase = vectorize_integration_container.vectorize_documents_usecase()
    result = usecase.execute(DocumentType.OFFERS)

    # Should handle HTTP error and convert to ExternalApiError
    assert result["processed"] == 0
    assert result["vectorized"] == 0
    assert result["errors"] == 1
    assert "Albert API error: 500" in result["error_details"][0]["exception"]


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
def test_vectorize_albert_empty_data_error(
    db, vectorize_integration_container, httpx_mock
):

    test_app_config = vectorize_integration_container.app_config()
    # Mock Albert API with empty data response using the factory
    empty_data_response = (
        MockApiResponseFactory.create_albert_embedding_response_empty_data()
    )
    mock_embedding_response(httpx_mock, test_app_config, empty_data_response)

    OfferFactory.create()
    usecase = vectorize_integration_container.vectorize_documents_usecase()
    result = usecase.execute(DocumentType.OFFERS)

    # Should handle empty data and raise ExternalApiError
    assert result["processed"] == 0
    assert result["vectorized"] == 0
    assert result["errors"] == 1
    error_message = result["error_details"][0]["exception"]
    assert "No embedding data in Albert API response" in error_message


@pytest.mark.httpx_mock(should_mock=lambda request: "albert" in str(request.url))
def test_vectorize_mark_as_processed_error(db, offer_setup, httpx_mock):

    usecase, repository, document_type = offer_setup

    # Mock Albert API for successful embedding generation
    app_config = AppConfig.from_django_settings()
    mock_embedding_response(httpx_mock, app_config)

    with patch.object(
        repository,
        "mark_as_processed",
        side_effect=Exception(DB_ERROR),
    ) as mocked_method:
        with pytest.raises(Exception, match=DB_ERROR):
            usecase.execute(document_type)
        mocked_method.assert_called_once()

    assert_offer_pending(processing=True)


def test_vectorize_mark_as_pending_error(db, offer_setup):
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
