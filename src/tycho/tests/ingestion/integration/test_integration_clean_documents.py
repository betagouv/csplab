"""Integration tests for CleanDocuments usecase with external adapters."""

import pytest

from domain.entities.document import DocumentType
from infrastructure.django_apps.shared.models.concours import ConcoursModel
from infrastructure.django_apps.shared.models.corps import CorpsModel
from tests.fixtures.clean_test_factories import (
    create_test_concours_document,
    create_test_concours_document_invalid_status,
    create_test_concours_document_old_year,
    create_test_corps_document,
    create_test_corps_document_fpt,
    create_test_corps_document_minarm,
)

# Test constants
DOCUMENTS_COUNT = 2
MIXED_DOCUMENTS_COUNT = 3


@pytest.mark.parametrize("document_type", [DocumentType.CORPS, DocumentType.CONCOURS])
@pytest.mark.django_db
def test_execute_handles_empty_documents(
    ingestion_integration_container, document_type
):
    """Test that empty document list is handled correctly."""
    clean_documents_usecase = ingestion_integration_container.clean_documents_usecase()

    # No documents in database
    doc_type = DocumentType.CORPS if document_type == "corps" else DocumentType.CONCOURS
    result = clean_documents_usecase.execute(doc_type)

    assert result["processed"] == 0
    assert result["cleaned"] == 0
    assert result["created"] == 0
    assert result["updated"] == 0
    assert result["errors"] == 0

    # Verify no entities are saved
    if document_type == DocumentType.CORPS:
        saved_entities = CorpsModel.objects.all()
    else:
        saved_entities = ConcoursModel.objects.all()
    assert saved_entities.count() == 0


@pytest.mark.parametrize("document_type", [DocumentType.CORPS, DocumentType.CONCOURS])
@pytest.mark.django_db
def test_execute_updates_existing_entities(
    ingestion_integration_container, document_type
):
    """Test that existing entities are updated correctly."""
    clean_documents_usecase = ingestion_integration_container.clean_documents_usecase()

    # Create raw document in database using repository
    document_repository = ingestion_integration_container.document_persister()

    if document_type == DocumentType.CORPS:
        document = create_test_corps_document(1)
    else:
        document = create_test_concours_document(1)

    document_repository.upsert_batch([document])

    # First execution - create entity
    result1 = clean_documents_usecase.execute(document_type)
    assert result1["created"] == 1
    assert result1["updated"] == 0

    # Second execution with same data - should update
    result2 = clean_documents_usecase.execute(document_type)
    assert result2["created"] == 0
    assert result2["updated"] == 1

    # Verify only one entity exists
    if document_type == DocumentType.CORPS:
        saved_entities = CorpsModel.objects.all()
    else:
        saved_entities = ConcoursModel.objects.all()
    assert len(saved_entities) == 1


@pytest.mark.django_db
def test_execute_filters_non_fpe_data(ingestion_integration_container):
    """Test that non-FPE corps data is properly filtered out."""
    clean_documents_usecase = ingestion_integration_container.clean_documents_usecase()
    document_repository = ingestion_integration_container.document_persister()

    # Create mixed data: 1 valid FPE + 1 invalid FPT
    valid_document = create_test_corps_document(1)
    invalid_document = create_test_corps_document_fpt(2)

    document_repository.upsert_batch([valid_document, invalid_document])

    result = clean_documents_usecase.execute(DocumentType.CORPS)

    # Verify statistics - only FPE documents should be cleaned and saved
    assert result["processed"] == DOCUMENTS_COUNT
    assert result["cleaned"] == 1
    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["errors"] == 0

    # Verify only valid Corps is saved
    saved_corps = CorpsModel.objects.all()
    assert saved_corps.count() == 1


@pytest.mark.django_db
def test_execute_retrieves_saved_corps_by_id(ingestion_integration_container):
    """Test that saved Corps entities can be retrieved by ID."""
    clean_documents_usecase = ingestion_integration_container.clean_documents_usecase()
    document_repository = ingestion_integration_container.document_persister()

    # Create raw document in database
    document = create_test_corps_document(1)
    document_repository.upsert_batch([document])

    # Execute CleanDocuments usecase
    result = clean_documents_usecase.execute(DocumentType.CORPS)
    assert result["created"] == 1

    # Verify saved corps can be retrieved by ID
    corps_repository = (
        ingestion_integration_container.shared_container.corps_repository()
    )

    # Get the actual ID from the fixture data
    actual_id = int(document.raw_data["identifiant"])
    retrieved_corps = corps_repository.find_by_id(actual_id)

    assert retrieved_corps is not None
    assert retrieved_corps.id == actual_id
    assert retrieved_corps.label is not None
    assert retrieved_corps.category is not None


@pytest.mark.django_db
def test_execute_handles_filtering_edge_cases(ingestion_integration_container):
    """Test various filtering scenarios."""
    clean_documents_usecase = ingestion_integration_container.clean_documents_usecase()
    document_repository = ingestion_integration_container.document_persister()

    # Create documents with different filtering conditions
    valid_document = create_test_corps_document(1)
    non_civil_servant_document = create_test_corps_document_fpt(2)
    minarm_document = create_test_corps_document_minarm(3)

    document_repository.upsert_batch(
        [valid_document, non_civil_servant_document, minarm_document]
    )

    result = clean_documents_usecase.execute(DocumentType.CORPS)

    assert result["processed"] == MIXED_DOCUMENTS_COUNT
    assert result["cleaned"] == 1
    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["errors"] == 0

    corps_repository = (
        ingestion_integration_container.shared_container.corps_repository()
    )
    saved_corps = corps_repository.get_all()
    assert len(saved_corps) == 1


@pytest.mark.django_db
def test_corps_repository_find_by_id_nonexistent(ingestion_integration_container):
    """Test find_by_id returns None for nonexistent Corps."""
    corps_repository = (
        ingestion_integration_container.shared_container.corps_repository()
    )

    nonexistent_corps = corps_repository.find_by_id(99999)

    assert nonexistent_corps is None


@pytest.mark.django_db
def test_corps_repository_get_all_empty(ingestion_integration_container):
    """Test get_all returns empty list when no Corps exist."""
    corps_repository = (
        ingestion_integration_container.shared_container.corps_repository()
    )

    all_corps = corps_repository.get_all()

    assert len(all_corps) == 0
    assert isinstance(all_corps, list)


@pytest.mark.django_db
def test_execute_creates_concours_successfully(ingestion_integration_container):
    """Test that valid concours documents are processed and saved."""
    clean_documents_usecase = ingestion_integration_container.clean_documents_usecase()
    document_repository = ingestion_integration_container.document_persister()

    valid_documents = [
        create_test_concours_document(1),
        create_test_concours_document(2),
    ]

    document_repository.upsert_batch(valid_documents)

    result = clean_documents_usecase.execute(DocumentType.CONCOURS)
    saved_concours = ConcoursModel.objects.all()

    assert result["processed"] == DOCUMENTS_COUNT
    assert result["cleaned"] == DOCUMENTS_COUNT
    assert result["created"] == DOCUMENTS_COUNT
    assert result["updated"] == 0
    assert result["errors"] == 0

    assert saved_concours.count() == DOCUMENTS_COUNT


@pytest.mark.django_db
def test_execute_filters_invalid_concours_status(ingestion_integration_container):
    """Test that concours with invalid status are filtered out."""
    clean_documents_usecase = ingestion_integration_container.clean_documents_usecase()
    document_repository = ingestion_integration_container.document_persister()

    # Mix valid and invalid status
    valid_document = create_test_concours_document(1)
    invalid_document = create_test_concours_document_invalid_status(2)

    test_documents = [valid_document, invalid_document]
    document_repository.upsert_batch(test_documents)

    result = clean_documents_usecase.execute(DocumentType.CONCOURS)

    # Only valid status should be processed
    assert result["processed"] == DOCUMENTS_COUNT
    assert result["cleaned"] == 1
    assert result["created"] == 1

    saved_concours = ConcoursModel.objects.all()
    assert saved_concours.count() == 1


@pytest.mark.django_db
def test_execute_filters_old_year_concours(ingestion_integration_container):
    """Test that concours with year <= 2024 are filtered out."""
    clean_documents_usecase = ingestion_integration_container.clean_documents_usecase()
    document_repository = ingestion_integration_container.document_persister()

    # Create concours with different years
    new_document = create_test_concours_document(1)
    old_document = create_test_concours_document_old_year(2)

    test_documents = [new_document, old_document]
    document_repository.upsert_batch(test_documents)

    result = clean_documents_usecase.execute(DocumentType.CONCOURS)

    assert result["processed"] == DOCUMENTS_COUNT
    assert result["cleaned"] == 1
    assert result["created"] == 1

    saved_concours = ConcoursModel.objects.all()
    assert saved_concours.count() == 1


@pytest.mark.django_db
def test_execute_filters_concours_missing_required_fields(
    ingestion_integration_container,
):
    """Test that concours with missing required fields are filtered out."""
    clean_documents_usecase = ingestion_integration_container.clean_documents_usecase()
    document_repository = ingestion_integration_container.document_persister()

    valid_document = create_test_concours_document(1)

    # Create invalid document by modifying raw_data
    invalid_document = create_test_concours_document(2)
    invalid_document.raw_data["N° NOR"] = None  # Missing required field

    test_documents = [valid_document, invalid_document]
    document_repository.upsert_batch(test_documents)

    result = clean_documents_usecase.execute(DocumentType.CONCOURS)

    assert result["processed"] == DOCUMENTS_COUNT
    assert result["cleaned"] == 1
    assert result["created"] == 1

    saved_concours = ConcoursModel.objects.all()
    assert saved_concours.count() == 1


@pytest.mark.django_db
def test_concours_repository_find_by_id_nonexistent(ingestion_integration_container):
    """Test find_by_id returns None for nonexistent Concours."""
    concours_repository = (
        ingestion_integration_container.shared_container.concours_repository()
    )

    nonexistent_concours = concours_repository.find_by_id(99999)

    assert nonexistent_concours is None


@pytest.mark.django_db
def test_concours_repository_get_all_empty(ingestion_integration_container):
    """Test get_all returns empty list when no Concours exist."""
    concours_repository = (
        ingestion_integration_container.shared_container.concours_repository()
    )

    all_concours = concours_repository.get_all()

    assert len(all_concours) == 0
    assert isinstance(all_concours, list)
