"""Unit tests for CleanDocuments usecase.

IMPORTANT: Dependency Injection Override Timing
- Override timing is crucial with dependency-injector
- Always override BEFORE creating the usecase, not after
- Dependencies are resolved at creation time, not execution time
"""

import copy
from datetime import datetime, timezone

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

# Test constants for offers edge cases
OFFERS_TOTAL_DOCUMENTS = 6
OFFERS_VALID_DOCUMENTS = 4
OFFERS_ERROR_DOCUMENTS = 2


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
    repository.upsert_batch(documents, document_type)

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
        external_id="grade_test_1",
        raw_data={"test": "data"},
        type=DocumentType.GRADE,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
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
        ],
        DocumentType.CORPS,
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
        ],
        DocumentType.CONCOURS,
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

    # Valid FPE with multiple edge cases combined
    valid_fpe_data = copy.deepcopy(create_test_offer_document(1).raw_data)
    valid_fpe_data["reference"] = "fpe_edge_cases"
    valid_fpe_data["salaryRange"] = None  # Test no verse
    valid_fpe_data["contractType"] = None  # Test null contract
    valid_fpe_data["beginningDate"] = None  # Test missing beginning date
    valid_fpe = Document(
        external_id="fpe_edge_cases",
        raw_data=valid_fpe_data,
        type=DocumentType.OFFERS,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    # Valid FPT with TERRITORIAL contract and edge cases
    valid_fpt_data = copy.deepcopy(create_test_offer_document(1).raw_data)
    valid_fpt_data["reference"] = "fpt_territorial"
    valid_fpt_data["salaryRange"]["clientCode"] = "Versant_FPT"
    valid_fpt_data["contractType"]["clientCode"] = "NAT_TERRITORIAL"
    valid_fpt_data["country"] = []  # Test missing localisation
    valid_fpt_data["region"] = []
    valid_fpt_data["department"] = []
    valid_fpt = Document(
        external_id="fpt_territorial",
        raw_data=valid_fpt_data,
        type=DocumentType.OFFERS,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    # Valid FPH with CONTRACTUELS and URL/date edge cases
    valid_fph_data = copy.deepcopy(create_test_offer_document(3).raw_data)
    valid_fph_data["reference"] = "fph_contractuels"
    valid_fph_data["salaryRange"]["clientCode"] = "Versant_FPH"
    valid_fph_data["contractType"]["clientCode"] = "NAT_CONTRACTUELS"
    valid_fph_data["offerUrl"] = "invalid://url with spaces"  # Test invalid URL
    valid_fph_data["beginningDate"] = "invalid-date-format"  # Test invalid date
    valid_fph = Document(
        external_id="fph_contractuels",
        raw_data=valid_fph_data,
        type=DocumentType.OFFERS,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    # Valid document with unknown contract type
    unknown_contract_data = copy.deepcopy(create_test_offer_document(1).raw_data)
    unknown_contract_data["reference"] = "unknown_contract"
    unknown_contract_data["contractType"]["clientCode"] = (
        "UNKNOWN_TYPE"  # Test unknown contract type
    )
    valid_unknown_contract = Document(
        external_id="unknown_contract",
        raw_data=unknown_contract_data,
        type=DocumentType.OFFERS,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    # Invalid documents
    invalid_ref = Document(
        external_id="invalid_ref",
        raw_data={"reference": "", "department": [{"clientCode": "18"}]},
        type=DocumentType.OFFERS,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    invalid_dep_data = copy.deepcopy(create_test_offer_document(6).raw_data)
    invalid_dep_data["reference"] = "invalid_dep"
    invalid_dep_data["department"][0]["clientCode"] = "999"
    invalid_department = Document(
        external_id="invalid_dep",
        raw_data=invalid_dep_data,
        type=DocumentType.OFFERS,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    repository = ingestion_container.document_persister()
    repository.upsert_batch(
        [
            valid_fpe,
            valid_fpt,
            valid_fph,
            valid_unknown_contract,
            invalid_ref,
            invalid_department,
        ],
        DocumentType.OFFERS,
    )
    result = usecase.execute(DocumentType.OFFERS)

    assert result["processed"] == OFFERS_TOTAL_DOCUMENTS
    assert result["cleaned"] == OFFERS_VALID_DOCUMENTS
    assert result["created"] == OFFERS_VALID_DOCUMENTS
    assert result["updated"] == 0
    assert result["errors"] == OFFERS_ERROR_DOCUMENTS
