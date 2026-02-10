"""Integration tests for VectorizeDocuments usecase with external adapters."""

import pytest

from infrastructure.django_apps.shared.models.vectorized_document import (
    VectorizedDocumentModel,
)
from tests.fixtures.vectorize_test_factories import (
    INTEGRATION_ENTITIES_COUNT,
    create_test_concours_for_integration,
    create_test_corps_for_integration,
    create_test_offer_for_integration,
)


@pytest.mark.parametrize("entity_type", ["corps", "concours", "offer"])
def test_vectorize_entity_integration(db, ingestion_integration_container, entity_type):
    """Test vectorizing different entity types with Django persistence."""
    usecase = ingestion_integration_container.vectorize_documents_usecase()

    # Create and save entity via repository
    if entity_type == "corps":
        entity = create_test_corps_for_integration(1)
        repository = ingestion_integration_container.shared_container.corps_repository()
        save_result = repository.upsert_batch([entity])
    elif entity_type == "concours":
        entity = create_test_concours_for_integration(1)
        repository = (
            ingestion_integration_container.shared_container.concours_repository()
        )
        save_result = repository.upsert_batch([entity])
    else:  # offer
        entity = create_test_offer_for_integration(1)
        repository = (
            ingestion_integration_container.shared_container.offers_repository()
        )
        save_result = repository.upsert_batch([entity])

    if save_result["errors"]:
        raise Exception(f"Failed to save {entity_type} entity: {save_result['errors']}")

    # Vectorize the entity
    result = usecase.execute([entity])

    assert result["processed"] == 1
    assert result["vectorized"] == 1
    assert result["errors"] == 0
    assert len(result["error_details"]) == 0

    # Verify vector was saved to database
    saved_vectors = VectorizedDocumentModel.objects.all()
    assert saved_vectors.count() == 1

    vector = VectorizedDocumentModel.objects.get(document_id=entity.id)
    assert vector.embedding is not None
    assert len(vector.embedding) > 0
    assert vector.content is not None
    assert vector.metadata is not None


@pytest.mark.parametrize("entity_type", ["corps", "concours", "offer"])
def test_vectorize_multiple_entities_integration(
    db, ingestion_integration_container, entity_type
):
    """Test vectorizing multiple entities of the same type with Django persistence."""
    usecase = ingestion_integration_container.vectorize_documents_usecase()

    # Create and save entities via repository
    if entity_type == "corps":
        entities = [
            create_test_corps_for_integration(i)
            for i in range(1, INTEGRATION_ENTITIES_COUNT + 1)
        ]
        repository = ingestion_integration_container.shared_container.corps_repository()
    elif entity_type == "concours":
        entities = [
            create_test_concours_for_integration(i)
            for i in range(1, INTEGRATION_ENTITIES_COUNT + 1)
        ]
        repository = (
            ingestion_integration_container.shared_container.concours_repository()
        )
    else:  # offer
        entities = [
            create_test_offer_for_integration(i)
            for i in range(1, INTEGRATION_ENTITIES_COUNT + 1)
        ]
        repository = (
            ingestion_integration_container.shared_container.offers_repository()
        )

    save_result = repository.upsert_batch(entities)
    if save_result["errors"]:
        raise Exception(
            f"Failed to save {entity_type} entities: {save_result['errors']}"
        )

    # Vectorize the entities
    result = usecase.execute(entities)

    assert result["processed"] == INTEGRATION_ENTITIES_COUNT
    assert result["vectorized"] == INTEGRATION_ENTITIES_COUNT
    assert result["errors"] == 0
    assert len(result["error_details"]) == 0

    # Verify vectors were saved to database
    saved_vectors = VectorizedDocumentModel.objects.all()
    assert saved_vectors.count() == INTEGRATION_ENTITIES_COUNT

    for _, entity in enumerate(entities):
        vector = VectorizedDocumentModel.objects.get(document_id=entity.id)
        assert vector.embedding is not None
        assert len(vector.embedding) > 0
        assert vector.content is not None
        assert vector.metadata is not None


def test_vectorize_empty_list_integration(db, ingestion_integration_container):
    """Test that empty entity list is handled correctly."""
    usecase = ingestion_integration_container.vectorize_documents_usecase()

    result = usecase.execute([])

    assert result["processed"] == 0
    assert result["vectorized"] == 0
    assert result["errors"] == 0
    assert len(result["error_details"]) == 0

    saved_vectors = VectorizedDocumentModel.objects.all()
    assert saved_vectors.count() == 0


def test_vectorize_entity_updates_existing_document_integration(
    db,
    ingestion_integration_container,
):
    """Test that vectorizing the same entity twice updates the existing document."""
    usecase = ingestion_integration_container.vectorize_documents_usecase()

    # Create and save entity
    entity = create_test_corps_for_integration(1)
    repository = ingestion_integration_container.shared_container.corps_repository()
    save_result = repository.upsert_batch([entity])

    if save_result["errors"]:
        raise Exception(f"Failed to save Corps entity: {save_result['errors']}")

    # First vectorization
    result1 = usecase.execute([entity])

    assert result1["processed"] == 1
    assert result1["vectorized"] == 1
    assert result1["errors"] == 0

    saved_vectors = VectorizedDocumentModel.objects.all()
    assert saved_vectors.count() == 1

    first_vector = VectorizedDocumentModel.objects.get(document_id=entity.id)
    original_created_at = first_vector.created_at
    original_updated_at = first_vector.updated_at

    # Second vectorization (should update)
    result2 = usecase.execute([entity])

    assert result2["processed"] == 1
    assert result2["vectorized"] == 1
    assert result2["errors"] == 0

    saved_vectors = VectorizedDocumentModel.objects.all()
    assert saved_vectors.count() == 1

    updated_vector = VectorizedDocumentModel.objects.get(document_id=entity.id)

    assert updated_vector.created_at == original_created_at
    assert updated_vector.updated_at > original_updated_at

    assert updated_vector.embedding is not None
    assert len(updated_vector.embedding) > 0
    assert "Professeurs de lycée professionnel agricole" in updated_vector.content


def test_vectorize_mixed_entities_integration(db, ingestion_integration_container):
    """Test vectorizing mixed entity types with Django persistence."""
    usecase = ingestion_integration_container.vectorize_documents_usecase()

    corps_entity = CorpsFactory.create().to_entity()
    concours_entity = ConcoursFactory.create().to_entity()
    offer_entity = OfferFactory.create().to_entity()

    entities = [corps_entity, concours_entity, offer_entity]
    result = usecase.execute(entities)

    assert result["processed"] == len(entities)
    assert result["vectorized"] == len(entities)
    assert result["errors"] == 0
    assert len(result["error_details"]) == 0

    assert VectorizedDocumentModel.objects.count() == len(entities)

    for document_id, document_type in [
        (corps_entity.id, DocumentType.CORPS),
        (concours_entity.id, DocumentType.CONCOURS),
        (offer_entity.id, DocumentType.OFFERS),
    ]:
        vector = VectorizedDocumentModel.objects.get(
            document_id=document_id, document_type=document_type
        )
        assert vector.embedding is not None
        assert len(vector.embedding) > 0
        assert vector.content is not None
        assert vector.metadata is not None
