"""Integration tests for CleanDocuments usecase with external adapters."""

import pytest

from domain.entities.document import DocumentType
from domain.exceptions.concours_errors import ConcoursDoesNotExist
from domain.exceptions.corps_errors import CorpsDoesNotExist
from domain.exceptions.offer_errors import OfferDoesNotExist
from infrastructure.django_apps.shared.models.concours import ConcoursModel
from infrastructure.django_apps.shared.models.corps import CorpsModel
from infrastructure.django_apps.shared.models.offer import OfferModel
from tests.fixtures.clean_test_factories import (
    create_test_concours_document,
    create_test_corps_document,
    create_test_offer_document,
)
from tests.fixtures.vectorize_test_factories import create_test_offer_for_integration

# Test constants
DOCUMENTS_COUNT = 2
MIXED_DOCUMENTS_COUNT = 3


@pytest.mark.parametrize(
    "document_type", [DocumentType.CORPS, DocumentType.CONCOURS, DocumentType.OFFERS]
)
@pytest.mark.django_db
def test_execute_handles_empty_documents(
    ingestion_integration_container, document_type
):
    """Test that empty document list is handled correctly."""
    clean_documents_usecase = ingestion_integration_container.clean_documents_usecase()

    # No documents in database
    result = clean_documents_usecase.execute(document_type)

    assert result["processed"] == 0
    assert result["cleaned"] == 0
    assert result["created"] == 0
    assert result["updated"] == 0
    assert result["errors"] == 0

    # Verify no entities are saved
    if document_type == DocumentType.CORPS:
        saved_entities = CorpsModel.objects.all()
    elif document_type == DocumentType.CONCOURS:
        saved_entities = ConcoursModel.objects.all()
    else:
        saved_entities = OfferModel.objects.all()
    assert saved_entities.count() == 0


@pytest.mark.parametrize(
    "document_type", [DocumentType.CORPS, DocumentType.CONCOURS, DocumentType.OFFERS]
)
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
    elif document_type == DocumentType.CONCOURS:
        document = create_test_concours_document(1)
    else:
        document = create_test_offer_document(1)

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
    elif document_type == DocumentType.CONCOURS:
        saved_entities = ConcoursModel.objects.all()
    else:
        saved_entities = OfferModel.objects.all()
    assert len(saved_entities) == 1


@pytest.mark.django_db
def test_find_by_id_nonexistent(ingestion_integration_container):
    """Test find_by_id returns None for nonexistent Corp, Concours, Offers."""
    corps_repository = (
        ingestion_integration_container.shared_container.corps_repository()
    )
    with pytest.raises(CorpsDoesNotExist):
        corps_repository.find_by_id(99999)
    concours_repository = (
        ingestion_integration_container.shared_container.concours_repository()
    )
    with pytest.raises(ConcoursDoesNotExist):
        concours_repository.find_by_id(99999)
    offers_repository = (
        ingestion_integration_container.shared_container.offers_repository()
    )
    with pytest.raises(OfferDoesNotExist):
        offers_repository.find_by_id(99999)


@pytest.mark.django_db
def test_repository_get_all_empty(ingestion_integration_container):
    """Test get_all returns empty list when no Corps exist."""
    corps_repository = (
        ingestion_integration_container.shared_container.corps_repository()
    )
    concours_repository = (
        ingestion_integration_container.shared_container.concours_repository()
    )

    offer_repository = (
        ingestion_integration_container.shared_container.offers_repository()
    )

    all_corps = corps_repository.get_all()
    all_concours = concours_repository.get_all()
    all_offers = offer_repository.get_all()

    assert len(all_corps) == 0
    assert isinstance(all_corps, list)
    assert len(all_concours) == 0
    assert isinstance(all_concours, list)
    assert len(all_offers) == 0
    assert isinstance(all_offers, list)


@pytest.mark.django_db
def test_upsert_batch_database_error(ingestion_integration_container):
    """Test that database errors are properly handled."""
    corps_repository = (
        ingestion_integration_container.shared_container.corps_repository()
    )
    concours_repository = (
        ingestion_integration_container.shared_container.concours_repository()
    )
    offers_repository = (
        ingestion_integration_container.shared_container.offers_repository()
    )

    corps = create_test_corps_document(1)
    corps.name = None  # no QA
    result_corps = corps_repository.upsert_batch([corps])

    concours = create_test_concours_document(1)
    concours.nor_original = None  # no QA
    result_concours = concours_repository.upsert_batch([concours])

    offer = create_test_offer_for_integration(1)
    offer.publication_date = "invalid_date"  # no QA
    result_offer = offers_repository.upsert_batch([offer])

    assert result_corps["created"] == 0
    assert result_corps["updated"] == 0
    assert len(result_corps["errors"]) == 1

    assert result_concours["created"] == 0
    assert result_concours["updated"] == 0
    assert len(result_concours["errors"]) == 1

    assert result_offer["created"] == 0
    assert result_offer["updated"] == 0
    assert len(result_offer["errors"]) == 1
