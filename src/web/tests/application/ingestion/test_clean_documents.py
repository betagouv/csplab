from datetime import datetime, timezone
from unittest.mock import Mock

import pytest

from domain.ingestion.entities.document import Document, DocumentType
from domain.ingestion.exceptions.document_error import UnsupportedDocumentTypeError
from tests.factories.ingestion.document_factory import DocumentFactory

THREE_DOCUMENTS_COUNT = 3


def mock_cleaning_result(entities, cleaning_errors):
    mock_result = Mock()
    mock_result.entities = entities
    mock_result.cleaning_errors = cleaning_errors
    return mock_result


@pytest.mark.parametrize(
    "document_type",
    [
        DocumentType.CORPS,
        DocumentType.CONCOURS,
        DocumentType.METIERS,
    ],
)
def test_clean_multiple_documents_success(clean_documents_usecase, document_type):
    document_repo = clean_documents_usecase.document_repository
    document_cleaner = clean_documents_usecase.document_cleaner

    if document_type == DocumentType.CORPS:
        documents = DocumentFactory.create_entity_batch(
            count=THREE_DOCUMENTS_COUNT, document_type=DocumentType.CORPS
        )
    elif document_type == DocumentType.CONCOURS:
        documents = DocumentFactory.create_entity_batch(
            count=THREE_DOCUMENTS_COUNT, document_type=DocumentType.CONCOURS
        )
    else:
        documents = DocumentFactory.create_entity_batch(
            count=THREE_DOCUMENTS_COUNT, document_type=DocumentType.METIERS
        )

    document_repo.upsert_batch(documents, document_type)

    document_cleaner.clean.return_value = mock_cleaning_result(documents, [])

    result = clean_documents_usecase.execute(document_type)

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
def test_clean_documents_with_empty_repository(clean_documents_usecase, document_type):
    document_cleaner = clean_documents_usecase.document_cleaner

    # Mock pour retourner des résultats vides
    document_cleaner.clean.return_value = mock_cleaning_result([], [])

    result = clean_documents_usecase.execute(document_type)

    assert result["processed"] == 0
    assert result["cleaned"] == 0
    assert result["created"] == 0
    assert result["updated"] == 0
    assert result["errors"] == 0


def test_execute_raises_error_for_unsupported_document_type(clean_documents_usecase):
    document_repo = clean_documents_usecase.document_repository

    grade_document = Document(
        external_id="grade_test_1",
        raw_data={"test": "data"},
        type=DocumentType.GRADE,
        created_at=datetime.now(timezone.utc),
    )

    document_repo.upsert_batch([grade_document], DocumentType.GRADE)

    with pytest.raises(UnsupportedDocumentTypeError) as exc_info:
        clean_documents_usecase.execute(DocumentType.GRADE)

    assert "GRADE" in str(exc_info.value)
