"""Unit test cases for VectorizeDocuments usecase.

IMPORTANT: Dependency Injection Override Timing
- Override timing is crucial with dependency-injector
- Always override BEFORE creating the usecase, not after
- Dependencies are resolved at creation time, not execution time
"""

from datetime import datetime

import pytest

from domain.entities.concours import Concours
from domain.entities.corps import Corps
from domain.entities.document import Document, DocumentType
from domain.entities.offer import Offer
from domain.interfaces.entity_interface import IEntity
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.department import Department
from domain.value_objects.diploma import Diploma
from domain.value_objects.label import Label
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.ministry import Ministry
from domain.value_objects.nor import NOR
from domain.value_objects.region import Region
from domain.value_objects.verse import Verse

# Test constants
MULTIPLE_ENTITIES_COUNT = 3
UNSUPPORTED_ENTITY_ID = 123
MIXED_ENTITIES_COUNT = 4
MIXED_ENTITIES_VECTORIZED = 3
MIXED_ENTITIES_INVALID_ID = 999


class UnsupportedEntity(IEntity):
    """Mock entity for testing unsupported source type."""

    def __init__(self, id: int):
        """Initialize with id."""
        self.id = id


def create_test_corps(entity_id: int = 1) -> Corps:
    """Create a test Corps entity."""
    return Corps(
        id=entity_id,
        code=f"CODE{entity_id}",
        category=Category.A,
        ministry=Ministry.MAA,
        diploma=Diploma(5),
        access_modalities=[AccessModality.CONCOURS_EXTERNE],
        label=Label(short_value="Test Corps", value="Test Corps Label"),
    )


def create_test_concours(entity_id: int = 1) -> Concours:
    """Create a test Concours entity."""
    return Concours(
        id=entity_id,
        nor_original=NOR("AGRS2400001A"),
        nor_list=[NOR("AGRS2400001A")],
        category=Category.A,
        ministry=Ministry.MAA,
        access_modality=[AccessModality.CONCOURS_EXTERNE],
        corps="Test Corps",
        grade="Test Grade",
        written_exam_date=None,
        open_position_number=10,
    )


def create_test_offer(entity_id: int = 1):
    """Create a test Offer entity."""
    return Offer(
        id=entity_id,
        external_id=f"OFFER_{entity_id:03d}",
        verse=Verse.FPE,
        titre="Développeur Python Senior",
        profile="Profil technique avec expertise Python",
        category=Category.A,
        localisation=Localisation(
            region=Region.ILE_DE_FRANCE, department=Department.PARIS
        ),
        limit_date=LimitDate(datetime(2024, 12, 31)),
    )


def create_test_document(
    entity_id: int = 1, doc_type: DocumentType = DocumentType.GRADE
) -> Document:
    """Create a test Document entity."""
    return Document(
        id=entity_id,
        external_id=f"test_doc_{entity_id}",
        raw_data={"content": f"Test document content {entity_id}"},
        type=doc_type,
        created_at=datetime.now(),
        updated_at=datetime.now(),
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
