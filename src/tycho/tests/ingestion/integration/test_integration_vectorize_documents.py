"""Integration tests for VectorizeDocuments usecase with external adapters."""

import pytest

from infrastructure.django_apps.shared.models import vectorized_document
from tests.fixtures.vectorize_test_factories import (
    INTEGRATION_ENTITIES_COUNT,
    create_test_concours_for_integration,
    create_test_corps_for_integration,
    create_test_offer_for_integration,
)


@pytest.mark.parametrize("entity_type", ["corps", "concours", "offer"])
@pytest.mark.django_db
def test_vectorize_entity_integration(ingestion_integration_container, entity_type):
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
    saved_vectors = vectorized_document.VectorizedDocumentModel.objects.all()
    assert saved_vectors.count() == 1

    vector = vectorized_document.VectorizedDocumentModel.objects.get(
        document_id=entity.id
    )
    assert vector.embedding is not None
    assert len(vector.embedding) > 0
    assert vector.content is not None
    assert vector.metadata is not None


@pytest.mark.parametrize("entity_type", ["corps", "concours", "offer"])
@pytest.mark.django_db
def test_vectorize_multiple_entities_integration(
    ingestion_integration_container, entity_type
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
    saved_vectors = vectorized_document.VectorizedDocumentModel.objects.all()
    assert saved_vectors.count() == INTEGRATION_ENTITIES_COUNT

    for _, entity in enumerate(entities):
        vector = vectorized_document.VectorizedDocumentModel.objects.get(
            document_id=entity.id
        )
        assert vector.embedding is not None
        assert len(vector.embedding) > 0
        assert vector.content is not None
        assert vector.metadata is not None


@pytest.mark.django_db
def test_vectorize_empty_list_integration(ingestion_integration_container):
    """Test that empty entity list is handled correctly."""
    usecase = ingestion_integration_container.vectorize_documents_usecase()

    result = usecase.execute([])

    assert result["processed"] == 0
    assert result["vectorized"] == 0
    assert result["errors"] == 0
    assert len(result["error_details"]) == 0

    saved_vectors = vectorized_document.VectorizedDocumentModel.objects.all()
    assert saved_vectors.count() == 0


@pytest.mark.django_db
def test_vectorize_entity_updates_existing_document_integration(
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

    saved_vectors = vectorized_document.VectorizedDocumentModel.objects.all()
    assert saved_vectors.count() == 1

    first_vector = vectorized_document.VectorizedDocumentModel.objects.get(
        document_id=entity.id
    )
    original_created_at = first_vector.created_at
    original_updated_at = first_vector.updated_at

    # Second vectorization (should update)
    result2 = usecase.execute([entity])

    assert result2["processed"] == 1
    assert result2["vectorized"] == 1
    assert result2["errors"] == 0

    saved_vectors = vectorized_document.VectorizedDocumentModel.objects.all()
    assert saved_vectors.count() == 1

    updated_vector = vectorized_document.VectorizedDocumentModel.objects.get(
        document_id=entity.id
    )

    assert updated_vector.created_at == original_created_at
    assert updated_vector.updated_at > original_updated_at

    assert updated_vector.embedding is not None
    assert len(updated_vector.embedding) > 0
    assert "Professeurs de lycée professionnel agricole" in updated_vector.content


@pytest.mark.django_db
def test_vectorize_mixed_entities_integration(ingestion_integration_container):
    """Test vectorizing mixed entity types with Django persistence."""
    usecase = ingestion_integration_container.vectorize_documents_usecase()

    # Create and save different entity types
    corps_entity = create_test_corps_for_integration(1)
    concours_entity = create_test_concours_for_integration(2)

    # Save each entity via its repository
    corps_repo = ingestion_integration_container.shared_container.corps_repository()
    concours_repo = (
        ingestion_integration_container.shared_container.concours_repository()
    )

    corps_result = corps_repo.upsert_batch([corps_entity])
    concours_result = concours_repo.upsert_batch([concours_entity])

    if corps_result["errors"] or concours_result["errors"]:
        raise Exception("Failed to save entities")

    # Vectorize all entities
    entities = [corps_entity, concours_entity]
    result = usecase.execute(entities)

    assert result["processed"] == INTEGRATION_ENTITIES_COUNT
    assert result["vectorized"] == INTEGRATION_ENTITIES_COUNT
    assert result["errors"] == 0
    assert len(result["error_details"]) == 0

    # Verify all vectors were saved
    saved_vectors = vectorized_document.VectorizedDocumentModel.objects.all()
    assert saved_vectors.count() == INTEGRATION_ENTITIES_COUNT

    for entity in entities:
        vector = vectorized_document.VectorizedDocumentModel.objects.get(
            document_id=entity.id
        )
        assert vector.embedding is not None
        assert len(vector.embedding) > 0
        assert vector.content is not None
        assert vector.metadata is not None
