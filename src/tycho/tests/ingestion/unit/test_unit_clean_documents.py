"""Unit tests for CleanDocuments usecase.

IMPORTANT: Dependency Injection Override Timing
- Override timing is crucial with dependency-injector
- Always override BEFORE creating the usecase, not after
- Dependencies are resolved at creation time, not execution time
"""

from datetime import datetime
from unittest.mock import Mock

import pytest

from domain.entities.document import Document, DocumentType
from domain.exceptions.document_error import UnsupportedDocumentTypeError
from tests.fixtures.clean_test_factories import (
    MIXED_DOCUMENTS_CLEANED,
    MULTIPLE_DOCUMENTS_COUNT,
    create_test_concours_document,
    create_test_concours_document_invalid_status,
    create_test_concours_document_old_year,
    create_test_corps_document,
    create_test_corps_document_fpt,
    create_test_corps_document_minarm,
)

REFERENCE_YEAR = 2024


@pytest.mark.parametrize("document_type", [DocumentType.CORPS, DocumentType.CONCOURS])
def test_clean_documents_success(ingestion_container, document_type):
    """Test cleaning different document types successfully."""
    usecase = ingestion_container.clean_documents_usecase()

    # Create test document based on type
    if document_type == DocumentType.CORPS:
        document = create_test_corps_document()
    else:  # concours
        document = create_test_concours_document()

    # Add document to repository
    repository = ingestion_container.document_persister()
    repository.upsert_batch([document], document_type)

    result = usecase.execute(document_type)

    assert result["processed"] == 1
    assert result["cleaned"] == 1
    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["errors"] == 0


@pytest.mark.parametrize("document_type", [DocumentType.CORPS, DocumentType.CONCOURS])
def test_clean_multiple_documents_success(ingestion_container, document_type):
    """Test cleaning multiple documents of the same type."""
    usecase = ingestion_container.clean_documents_usecase()

    # Create multiple documents
    if document_type == DocumentType.CORPS:
        documents = [
            create_test_corps_document(i)
            for i in range(1, MULTIPLE_DOCUMENTS_COUNT + 1)
        ]
    else:  # concours
        documents = [
            create_test_concours_document(i)
            for i in range(1, MULTIPLE_DOCUMENTS_COUNT + 1)
        ]

    # Add documents to repository
    repository = ingestion_container.document_persister()
    repository.upsert_batch(documents, document_type)

    result = usecase.execute(document_type)

    assert result["processed"] == MULTIPLE_DOCUMENTS_COUNT
    assert result["cleaned"] == MULTIPLE_DOCUMENTS_COUNT
    assert result["created"] == MULTIPLE_DOCUMENTS_COUNT
    assert result["updated"] == 0
    assert result["errors"] == 0


def test_clean_documents_with_empty_repository(ingestion_container):
    """Test cleaning when no documents exist returns zero statistics."""
    usecase = ingestion_container.clean_documents_usecase()

    result = usecase.execute(DocumentType.CORPS)

    assert result["processed"] == 0
    assert result["cleaned"] == 0
    assert result["created"] == 0
    assert result["updated"] == 0
    assert result["errors"] == 0


def test_clean_corps_documents_filters_non_fpe_data(ingestion_container):
    """Test that non-FPE corps data is properly filtered out."""
    usecase = ingestion_container.clean_documents_usecase()

    # Create mixed data: 1 valid FPE + 1 invalid FPT
    valid_document = create_test_corps_document(1)
    invalid_document = create_test_corps_document_fpt(2)

    repository = ingestion_container.document_persister()
    repository.upsert_batch([valid_document, invalid_document], DocumentType.CORPS)

    result = usecase.execute(DocumentType.CORPS)

    assert result["processed"] == MIXED_DOCUMENTS_CLEANED
    assert result["cleaned"] == 1
    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["errors"] == 0


def test_clean_corps_documents_filters_minarm_ministry(ingestion_container):
    """Test that MINARM ministry is properly filtered out."""
    usecase = ingestion_container.clean_documents_usecase()

    # Create mixed data: 1 valid + 1 MINARM
    valid_document = create_test_corps_document(1)
    minarm_document = create_test_corps_document_minarm(2)

    repository = ingestion_container.document_persister()
    repository.upsert_batch([valid_document, minarm_document], DocumentType.CORPS)

    result = usecase.execute(DocumentType.CORPS)

    assert result["processed"] == MIXED_DOCUMENTS_CLEANED
    assert result["cleaned"] == 1
    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["errors"] == 0


def test_clean_concours_documents_filters_invalid_status(ingestion_container):
    """Test that CONCOURS with invalid status are filtered out."""
    usecase = ingestion_container.clean_documents_usecase()

    # Create mixed data: 1 valid + 1 invalid status
    valid_document = create_test_concours_document(1)
    invalid_document = create_test_concours_document_invalid_status(2)

    repository = ingestion_container.document_persister()
    repository.upsert_batch([valid_document, invalid_document], DocumentType.CONCOURS)

    result = usecase.execute(DocumentType.CONCOURS)

    assert result["processed"] == MIXED_DOCUMENTS_CLEANED
    assert result["cleaned"] == 1
    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["errors"] == 0


def test_clean_concours_documents_filters_old_year(ingestion_container):
    """Test that CONCOURS with old year are filtered out."""
    usecase = ingestion_container.clean_documents_usecase()

    # Create mixed data: 1 valid + 1 old year
    valid_document = create_test_concours_document(1)
    old_document = create_test_concours_document_old_year(2)

    repository = ingestion_container.document_persister()
    repository.upsert_batch([valid_document, old_document], DocumentType.CONCOURS)

    result = usecase.execute(DocumentType.CONCOURS)

    assert result["processed"] == MIXED_DOCUMENTS_CLEANED
    assert result["cleaned"] == 1
    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["errors"] == 0


def test_clean_documents_error_handling_save_errors(ingestion_container):
    """Test error handling for save operations."""
    ENTITY_ID = 10001

    # Create test document
    document = create_test_corps_document()
    repository = ingestion_container.document_persister()
    repository.upsert_batch([document], DocumentType.CORPS)

    # Mock the corps repository to return errors
    mock_repository = Mock()
    mock_repository.upsert_batch.return_value = {
        "created": 0,
        "updated": 0,
        "errors": [
            {"entity_id": ENTITY_ID, "error": "Database connection failed"},
        ],
    }

    # Override BEFORE creating the usecase
    ingestion_container.corps_repository.override(mock_repository)
    usecase = ingestion_container.clean_documents_usecase()

    result = usecase.execute(DocumentType.CORPS)

    assert result["processed"] == 1
    assert result["cleaned"] == 1
    assert result["created"] == 0
    assert result["updated"] == 0
    assert result["errors"] == 1
    assert len(result["error_details"]) == 1
    assert result["error_details"][0]["entity_id"] == ENTITY_ID


def test_clean_documents_mixed_success_and_errors(ingestion_container):
    """Test mixed success and error scenarios."""
    # Create test documents
    documents = [create_test_corps_document(i) for i in range(1, 3)]
    repository = ingestion_container.document_persister()
    repository.upsert_batch(documents, DocumentType.CORPS)

    # Mock the corps repository to return mixed results
    mock_repository = Mock()
    mock_repository.upsert_batch.return_value = {
        "created": 1,
        "updated": 0,
        "errors": [
            {"entity_id": 10002, "error": "Validation error"},
        ],
    }

    # Override BEFORE creating the usecase
    ingestion_container.corps_repository.override(mock_repository)
    usecase = ingestion_container.clean_documents_usecase()

    result = usecase.execute(DocumentType.CORPS)

    assert result["processed"] == MIXED_DOCUMENTS_CLEANED
    assert result["cleaned"] == MIXED_DOCUMENTS_CLEANED
    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["errors"] == 1
    assert len(result["error_details"]) == 1


def test_execute_raises_error_for_unsupported_document_type(ingestion_container):
    """Test that UnsupportedDocumentTypeError is raised for unsupported types."""
    # Create a GRADE document (unsupported)
    grade_document = Document(
        id=1,
        external_id="grade_test_1",
        raw_data={"test": "data"},
        type=DocumentType.GRADE,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    repository = ingestion_container.document_persister()
    repository.upsert_batch([grade_document], DocumentType.GRADE)

    usecase = ingestion_container.clean_documents_usecase()

    with pytest.raises(UnsupportedDocumentTypeError) as exc_info:
        usecase.execute(DocumentType.GRADE)

    assert "GRADE" in str(exc_info.value)
