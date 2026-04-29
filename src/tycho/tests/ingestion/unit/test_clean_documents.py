from datetime import datetime, timezone
from unittest.mock import Mock

import pytest

from application.ingestion.usecases.clean_documents import CleanDocumentsUsecase
from domain.entities.document import Document, DocumentType
from domain.exceptions.document_error import UnsupportedDocumentTypeError
from infrastructure.gateways.shared.logger import LoggerService
from tests.fixtures.clean_test_factories import (
    THREE_DOCUMENTS_COUNT,
    create_test_concours_document,
    create_test_corps_document,
    create_test_metier_document,
)
from tests.utils.in_memory_concours_repository import InMemoryConcoursRepository
from tests.utils.in_memory_corps_repository import InMemoryCorpsRepository
from tests.utils.in_memory_document_repository import InMemoryDocumentRepository
from tests.utils.in_memory_metier_repository import InMemoryMetierRepository
from tests.utils.in_memory_offers_repository import InMemoryOffersRepository


def mock_cleaning_result(entities, cleaning_errors):
    mock_result = Mock()
    mock_result.entities = entities
    mock_result.cleaning_errors = cleaning_errors
    return mock_result


@pytest.fixture
def clean_documents():
    logger_service = LoggerService()
    document_repo = InMemoryDocumentRepository()

    document_cleaner = Mock()
    document_cleaner.clean.return_value = mock_cleaning_result([], [])

    repository_factory = Mock()

    corps_repo = InMemoryCorpsRepository()
    concours_repo = InMemoryConcoursRepository()
    metier_repo = InMemoryMetierRepository()
    offers_repo = InMemoryOffersRepository()

    def get_repository(document_type):
        if document_type == DocumentType.CORPS:
            return corps_repo
        elif document_type == DocumentType.CONCOURS:
            return concours_repo
        elif document_type == DocumentType.METIERS:
            return metier_repo
        elif document_type == DocumentType.OFFERS:
            return offers_repo
        else:
            raise UnsupportedDocumentTypeError(
                f"Unsupported document type: {document_type}"
            )

    repository_factory.get_repository.side_effect = get_repository

    usecase = CleanDocumentsUsecase(
        document_repository=document_repo,
        document_cleaner=document_cleaner,
        repository_factory=repository_factory,
        logger=logger_service,
    )

    return (
        usecase,
        document_repo,
        document_cleaner,
        repository_factory,
        {
            DocumentType.CORPS: corps_repo,
            DocumentType.CONCOURS: concours_repo,
            DocumentType.METIERS: metier_repo,
            DocumentType.OFFERS: offers_repo,
        },
    )


@pytest.mark.parametrize(
    "document_type",
    [
        DocumentType.CORPS,
        DocumentType.CONCOURS,
        DocumentType.METIERS,
    ],
)
def test_clean_multiple_documents_success(clean_documents, document_type):
    usecase, document_repo, document_cleaner, _, repositories = clean_documents

    if document_type == DocumentType.CORPS:
        documents = [
            create_test_corps_document(i) for i in range(1, THREE_DOCUMENTS_COUNT + 1)
        ]
    elif document_type == DocumentType.CONCOURS:
        documents = [
            create_test_concours_document(i)
            for i in range(1, THREE_DOCUMENTS_COUNT + 1)
        ]
    else:
        documents = [
            create_test_metier_document(i) for i in range(1, THREE_DOCUMENTS_COUNT + 1)
        ]

    document_repo.upsert_batch(documents, document_type)

    if document_type != DocumentType.METIERS:
        document_cleaner.clean.return_value = mock_cleaning_result(documents, [])

    result = usecase.execute(document_type)

    assert result["processed"] == THREE_DOCUMENTS_COUNT
    assert result["cleaned"] == THREE_DOCUMENTS_COUNT
    assert result["created"] == THREE_DOCUMENTS_COUNT
    assert result["updated"] == 0
    assert result["errors"] == 0


@pytest.mark.parametrize(
    "document_type",
    [
        DocumentType.CORPS,
        DocumentType.CONCOURS,
        DocumentType.METIERS,
    ],
)
def test_clean_documents_with_empty_repository(clean_documents, document_type):
    usecase, document_repo, document_cleaner, _, _ = clean_documents

    # Mock pour retourner des résultats vides
    document_cleaner.clean.return_value = mock_cleaning_result([], [])

    result = usecase.execute(document_type)

    assert result["processed"] == 0
    assert result["cleaned"] == 0
    assert result["created"] == 0
    assert result["updated"] == 0
    assert result["errors"] == 0


def test_execute_raises_error_for_unsupported_document_type(clean_documents):
    usecase, document_repo, _, _, _ = clean_documents

    grade_document = Document(
        external_id="grade_test_1",
        raw_data={"test": "data"},
        type=DocumentType.GRADE,
        created_at=datetime.now(timezone.utc),
    )

    document_repo.upsert_batch([grade_document], DocumentType.GRADE)

    with pytest.raises(UnsupportedDocumentTypeError) as exc_info:
        usecase.execute(DocumentType.GRADE)

    assert "GRADE" in str(exc_info.value)
