"""Unit test cases for VectorizeDocuments usecase.

IMPORTANT: Dependency Injection Override Timing
- Override timing is crucial with dependency-injector
- Always override BEFORE creating the usecase, not after
- Dependencies are resolved at creation time, not execution time
"""

import pytest

from domain.entities.document import DocumentType
from tests.fixtures.vectorize_test_factories import (
    MIXED_ENTITIES_COUNT,
    MIXED_ENTITIES_INVALID_ID,
    MIXED_ENTITIES_VECTORIZED,
    MULTIPLE_ENTITIES_COUNT,
    UNSUPPORTED_ENTITY_ID,
    UnsupportedEntity,
    create_test_concours,
    create_test_corps,
    create_test_document,
    create_test_offer,
)


@pytest.mark.parametrize("entity_type", ["corps", "concours", "offer"])
def test_vectorize_entity_success(ingestion_container, entity_type):
    """Test vectorizing different entity types successfully."""
    usecase = ingestion_container.vectorize_documents_usecase()

    if entity_type == "corps":
        entity = create_test_corps()
    elif entity_type == "concours":
        entity = create_test_concours()
    else:  # offer
        entity = create_test_offer()

    result = usecase.execute([entity])

    assert result["processed"] == 1
    assert result["vectorized"] == 1
    assert result["errors"] == 0


@pytest.mark.parametrize("entity_type", ["corps", "concours", "offer"])
def test_vectorize_multiple_entities_success(ingestion_container, entity_type):
    """Test vectorizing multiple entities of the same type."""
    usecase = ingestion_container.vectorize_documents_usecase()

    # Create multiple entities
    if entity_type == "corps":
        entities = [create_test_corps(i) for i in range(1, MULTIPLE_ENTITIES_COUNT + 1)]
    elif entity_type == "concours":
        entities = [
            create_test_concours(i) for i in range(1, MULTIPLE_ENTITIES_COUNT + 1)
        ]
    else:  # offer
        entities = [create_test_offer(i) for i in range(1, MULTIPLE_ENTITIES_COUNT + 1)]

    result = usecase.execute(entities)

    assert result["processed"] == MULTIPLE_ENTITIES_COUNT
    assert result["vectorized"] == MULTIPLE_ENTITIES_COUNT
    assert result["errors"] == 0


def test_vectorize_entity_error_handling_unsupported_type(ingestion_container):
    """Test error handling for unsupported entity types."""
    usecase = ingestion_container.vectorize_documents_usecase()

    entities = [UnsupportedEntity(id=UNSUPPORTED_ENTITY_ID)]
    result = usecase.execute(entities)

    assert result["processed"] == 1
    assert result["vectorized"] == 0
    assert result["errors"] == 1
    assert len(result["error_details"]) == 1

    error_detail = result["error_details"][0]
    assert error_detail["source_type"] == "UnsupportedEntity"
    assert error_detail["source_id"] == UNSUPPORTED_ENTITY_ID
    assert "error" in error_detail


def test_vectorize_document_unsupported_type(ingestion_container):
    """Test vectorizing unsupported document type."""
    usecase = ingestion_container.vectorize_documents_usecase()

    document = create_test_document(doc_type=DocumentType.GRADE)
    result = usecase.execute([document])

    assert result["processed"] == 1
    assert result["vectorized"] == 0
    assert result["errors"] == 1
    assert (
        "Content extraction not implemented for document type GRADE"
        in result["error_details"][0]["error"]
    )


def test_vectorize_mixed_entities_with_errors(ingestion_container):
    """Test vectorizing mixed entities with some errors."""
    usecase = ingestion_container.vectorize_documents_usecase()

    # Mix of valid and invalid entities
    valid_corps = create_test_corps(1)
    valid_concours = create_test_concours(2)
    valid_offer = create_test_offer(3)
    invalid_entity = UnsupportedEntity(id=MIXED_ENTITIES_INVALID_ID)

    entities = [valid_corps, valid_concours, valid_offer, invalid_entity]
    result = usecase.execute(entities)

    assert result["processed"] == MIXED_ENTITIES_COUNT
    assert result["vectorized"] == MIXED_ENTITIES_VECTORIZED
    assert result["errors"] == 1
    assert len(result["error_details"]) == 1
    assert result["error_details"][0]["source_type"] == "UnsupportedEntity"
