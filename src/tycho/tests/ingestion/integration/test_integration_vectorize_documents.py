from unittest.mock import patch

import pytest

from domain.entities.document import DocumentType
from domain.exceptions.document_error import UnsupportedDocumentTypeError
from infrastructure.django_apps.shared.models.offer import OfferModel
from infrastructure.django_apps.shared.models.vectorized_document import (
    VectorizedDocumentModel,
)
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.corps_factory import CorpsFactory
from tests.factories.offer_factory import OfferFactory

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
def offer_setup_fixture(db, ingestion_integration_container):
    document_type = DocumentType.OFFERS
    usecase = ingestion_integration_container.vectorize_documents_usecase()
    repository = usecase.repository_factory.get_repository(document_type)
    factories_mapper[document_type].create()
    return usecase, repository, document_type


@pytest.mark.parametrize(
    "document_type", [DocumentType.CORPS, DocumentType.CONCOURS, DocumentType.OFFERS]
)
def test_vectorize_entity_integration(
    db, ingestion_integration_container, document_type
):
    usecase = ingestion_integration_container.vectorize_documents_usecase()
    documents = factories_mapper[document_type].create_batch(2)

    result = usecase.execute(document_type)

    assert_success_result(result, expected_count=len(documents))

    # With Qdrant, documents are not stored in VectorizedDocumentModel anymore
    # Instead, verify they are in Qdrant by doing a search
    vector_repo = ingestion_integration_container.vector_repository()
    search_results = vector_repo.semantic_search(
        query_embedding=[0.1] * 1536,  # Mock embedding for search
        limit=10,
        filters={"document_type": document_type.value},
    )

    assert len(search_results) == len(documents)
    for result in search_results:
        assert result.document.document_type == document_type
        assert result.document.content is not None
        assert result.document.metadata is not None
        assert result.score >= 0.0


def test_vectorize_empty_list_integration(db, ingestion_integration_container):
    usecase = ingestion_integration_container.vectorize_documents_usecase()

    result = usecase.execute(DocumentType.OFFERS)

    assert_success_result(result, expected_count=0)
    assert_nothing_vectorized()


def test_vectorize_limit(db, ingestion_integration_container):
    limit = 2
    OfferFactory.create_batch(limit + 1)
    usecase = ingestion_integration_container.vectorize_documents_usecase()
    result = usecase.execute(DocumentType.OFFERS, limit=limit)

    assert_success_result(result, expected_count=limit)

    # With Qdrant, verify documents are stored by searching
    vector_repo = ingestion_integration_container.vector_repository()
    search_results = vector_repo.semantic_search(
        query_embedding=[0.1] * 1536,  # Mock embedding for search
        limit=10,
        filters={"document_type": DocumentType.OFFERS.value},
    )
    assert len(search_results) == limit

    assert OfferModel.objects.filter(processed_at__isnull=False).count() == limit


def test_vectorize_get_pending_processing_error(offer_setup):
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


def test_vectorize_vectorize_single_source_error(offer_setup):
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


def test_vectorize_upsert_batch_error(offer_setup):
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


def test_vectorize_mark_as_processed_error(offer_setup):
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


def test_vectorize_mark_as_pending_error(offer_setup):
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
