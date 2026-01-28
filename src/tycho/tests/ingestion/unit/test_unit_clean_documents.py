"""Unit tests for CleanDocuments usecase.

IMPORTANT: Dependency Injection Override Timing
- Override timing is crucial with dependency-injector
- Always override BEFORE creating the usecase, not after
- Dependencies are resolved at creation time, not execution time
"""

import copy
from datetime import datetime

import pytest

from domain.entities.document import Document, DocumentType
from domain.exceptions.document_error import UnsupportedDocumentTypeError
from tests.fixtures.clean_test_factories import (
    THREE_DOCUMENTS_COUNT,
    TWO_DOCUMENTS_COUNT,
    create_test_concours_document,
    create_test_concours_document_invalid_status,
    create_test_concours_document_old_year,
    create_test_corps_document,
    create_test_corps_document_fpt,
    create_test_corps_document_minarm,
    create_test_offer_document,
)

REFERENCE_YEAR = 2024


@pytest.mark.parametrize(
    "document_type", [DocumentType.CORPS, DocumentType.CONCOURS, DocumentType.OFFERS]
)
def test_clean_multiple_documents_success(ingestion_container, document_type):
    """Test cleaning multiple documents of the same type."""
    usecase = ingestion_container.clean_documents_usecase()
    # Create multiple documents
    if document_type == DocumentType.CORPS:
        documents = [
            create_test_corps_document(i) for i in range(1, THREE_DOCUMENTS_COUNT + 1)
        ]
    elif document_type == DocumentType.CONCOURS:
        documents = [
            create_test_concours_document(i)
            for i in range(1, THREE_DOCUMENTS_COUNT + 1)
        ]
    else:  # offers
        documents = [
            create_test_offer_document(i) for i in range(1, THREE_DOCUMENTS_COUNT + 1)
        ]
    # Add documents to repository
    repository = ingestion_container.document_persister()
    repository.upsert_batch(documents)

    result = usecase.execute(document_type)

    assert result["processed"] == THREE_DOCUMENTS_COUNT
    assert result["cleaned"] == THREE_DOCUMENTS_COUNT
    assert result["created"] == THREE_DOCUMENTS_COUNT
    assert result["updated"] == 0
    assert result["errors"] == 0


@pytest.mark.parametrize(
    "document_type", [DocumentType.CORPS, DocumentType.CONCOURS, DocumentType.OFFERS]
)
def test_clean_documents_with_empty_repository(ingestion_container, document_type):
    """Test cleaning when no documents exist returns zero statistics."""
    usecase = ingestion_container.clean_documents_usecase()

    result = usecase.execute(document_type)

    assert result["processed"] == 0
    assert result["cleaned"] == 0
    assert result["created"] == 0
    assert result["updated"] == 0
    assert result["errors"] == 0


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


def test_clean_corps_filters_invalid_documents(ingestion_container):
    """Test that invalid corps data is properly filtered out."""
    usecase = ingestion_container.clean_documents_usecase()

    # Create mixed data: 1 valid FPE + 1 invalid FPT
    valid_document = create_test_corps_document(1)
    fpt_document = create_test_corps_document_fpt(8)
    minarm_document = create_test_corps_document_minarm(9)

    repository = ingestion_container.document_persister()
    repository.upsert_batch(
        [
            valid_document,
            fpt_document,
            minarm_document,
        ]
    )
    result = usecase.execute(DocumentType.CORPS)

    assert result["processed"] == THREE_DOCUMENTS_COUNT
    assert result["cleaned"] == 1
    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["errors"] == TWO_DOCUMENTS_COUNT


def test_clean_concours_filters_invalid_documents(ingestion_container):
    """Test that invalid concours data is properly filtered out."""
    usecase = ingestion_container.clean_documents_usecase()

    # Create mixed data: 1 valid FPE + 1 invalid FPT
    valid_document = create_test_concours_document(1)
    invalid_status_document = create_test_concours_document_invalid_status(4)
    old_document = create_test_concours_document_old_year(5)

    repository = ingestion_container.document_persister()
    repository.upsert_batch(
        [
            valid_document,
            invalid_status_document,
            old_document,
        ]
    )
    result = usecase.execute(DocumentType.CONCOURS)

    assert result["processed"] == THREE_DOCUMENTS_COUNT
    assert result["cleaned"] == 1
    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["errors"] == TWO_DOCUMENTS_COUNT


def test_clean_offers_filters_invalid_documents(ingestion_container):
    """Test that invalid offers data is properly filtered out."""
    usecase = ingestion_container.clean_documents_usecase()

    valid_document = create_test_offer_document(1)
    invalid_data = copy.deepcopy(valid_document.raw_data)
    invalid_data["reference"] = "offer_invalid_2"
    invalid_data["department"][0]["clientCode"] = "999"
    invalid_document = Document(
        id=2,
        external_id=invalid_data["reference"],
        raw_data=invalid_data,
        type=DocumentType.OFFERS,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    repository = ingestion_container.document_persister()
    repository.upsert_batch(
        [
            invalid_document,
        ]
    )
    result = usecase.execute(DocumentType.OFFERS)

    assert result["processed"] == 1
    assert result["cleaned"] == 0
    assert result["created"] == 0
    assert result["updated"] == 0
    assert result["errors"] == 1
