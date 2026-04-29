from unittest.mock import AsyncMock, Mock

import pytest

from application.ingestion.usecases.vectorize_documents import VectorizeDocumentsUsecase
from domain.entities.document import Document, DocumentType
from domain.exceptions.document_error import UnsupportedDocumentTypeError
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.corps_factory import CorpsFactory
from tests.factories.offer_factory import OfferFactory
from tests.utils.in_memory_vector_repository import InMemoryVectorRepository


@pytest.fixture
def vectorize_documents():
    logger_service = LoggerService()
    vector_repo = InMemoryVectorRepository(logger_service)

    text_extractor = Mock()
    text_extractor.extract_content.return_value = "Extracted text content"
    text_extractor.extract_metadata.return_value = {"key": "value"}

    embedding_generator = Mock()
    embedding_generator.generate_embedding = AsyncMock(return_value=[0.1, 0.2, 0.3])

    repository_factory = Mock()
    mock_source_repo = Mock()
    mock_source_repo.get_pending_processing.return_value = []
    mock_source_repo.mark_as_processed.return_value = None
    mock_source_repo.mark_as_pending.return_value = None
    repository_factory.get_repository.return_value = mock_source_repo

    usecase = VectorizeDocumentsUsecase(
        vector_repository=vector_repo,
        text_extractor=text_extractor,
        embedding_generator=embedding_generator,
        logger=logger_service,
        repository_factory=repository_factory,
    )

    return (
        usecase,
        vector_repo,
        text_extractor,
        embedding_generator,
        repository_factory,
        mock_source_repo,
    )


@pytest.mark.parametrize(
    "document_type", [DocumentType.CORPS, DocumentType.CONCOURS, DocumentType.OFFERS]
)
def test_execute_with_single_entity_success(
    db, vectorize_documents, document_type
):  # TO-DO make vectorize usecase independent from django ORM

    (
        usecase,
        _,
        text_extractor,
        embedding_generator,
        _,
        mock_source_repo,
    ) = vectorize_documents

    sample_source = None
    match document_type:
        case DocumentType.CORPS:
            sample_source = CorpsFactory.create().to_entity()
        case DocumentType.CONCOURS:
            sample_source = ConcoursFactory.create().to_entity()
        case DocumentType.OFFERS:
            sample_source = OfferFactory.build()

    mock_source_repo.get_pending_processing.return_value = [sample_source]

    result = usecase.execute(document_type)

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


def test_vectorize_single_source_with_unsupported_type(vectorize_documents):
    (
        usecase,
        _,
        _,
        _,
        _,
        _,
    ) = vectorize_documents

    unsupported_source = Mock()

    with pytest.raises(UnsupportedDocumentTypeError):
        usecase.vectorize_single_source(unsupported_source)


def test_vectorize_single_source_with_none_entity_id_raises_error(vectorize_documents):
    (
        usecase,
        _,
        _,
        _,
        _,
        _,
    ) = vectorize_documents

    source_with_none_id = Mock(spec=Document)
    source_with_none_id.id = None
    source_with_none_id.type = DocumentType.CORPS

    with pytest.raises(ValueError, match="Entity ID cannot be None"):
        usecase.vectorize_single_source(source_with_none_id)
