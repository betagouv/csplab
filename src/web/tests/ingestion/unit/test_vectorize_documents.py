from unittest.mock import Mock

import pytest

from domain.ingestion.entities.document import Document, DocumentType
from domain.ingestion.exceptions.document_error import UnsupportedDocumentTypeError
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.corps_factory import CorpsFactory
from tests.factories.metier_factory import MetierFactory
from tests.factories.offer_factory import OfferFactory


@pytest.mark.parametrize(
    "document_type",
    [
        DocumentType.CORPS,
        DocumentType.CONCOURS,
        DocumentType.OFFERS,
        DocumentType.METIERS,
    ],
)
def test_execute_with_single_entity_success(
    db, vectorize_documents_usecase, document_type
):  # TO-DO make vectorize usecase independent from django ORM

    text_extractor = vectorize_documents_usecase.text_extractor
    embedding_generator = vectorize_documents_usecase.embedding_generator
    mock_source_repo = (
        vectorize_documents_usecase.repository_factory.get_repository.return_value
    )

    sample_source = None
    match document_type:
        case DocumentType.CORPS:
            sample_source = CorpsFactory.create_entity()
        case DocumentType.CONCOURS:
            sample_source = ConcoursFactory.create_entity()
        case DocumentType.OFFERS:
            sample_source = OfferFactory.create_entity()
        case DocumentType.METIERS:
            sample_source = MetierFactory.create_entity()

    mock_source_repo.get_pending_processing.return_value = [sample_source]

    result = vectorize_documents_usecase.execute(document_type)

    assert result["processed"] == 1
    assert result["vectorized"] == 1
    assert result["errors"] == 0
    assert result["error_details"] == []

    text_extractor.extract_content.assert_called_once_with(sample_source)
    text_extractor.extract_metadata.assert_called_once_with(sample_source)
    embedding_generator.generate_embedding.assert_called_once_with(
        "Extracted text content"
    )
    mock_source_repo.mark_as_processed.assert_called_once()


def test_vectorize_single_source_with_unsupported_type(vectorize_documents_usecase):
    unsupported_source = Mock()

    with pytest.raises(UnsupportedDocumentTypeError):
        vectorize_documents_usecase.vectorize_single_source(unsupported_source)


def test_vectorize_single_source_with_none_entity_id_raises_error(
    vectorize_documents_usecase,
):

    source_with_none_id = Mock(spec=Document)
    source_with_none_id.entity_id = None
    source_with_none_id.type = DocumentType.CORPS

    with pytest.raises(ValueError, match="Entity ID cannot be None"):
        vectorize_documents_usecase.vectorize_single_source(source_with_none_id)
