"""Shared factory functions and constants for vectorize documents tests."""

from datetime import datetime

from domain.entities.concours import Concours
from domain.entities.corps import Corps
from domain.entities.document import Document, DocumentType
from domain.entities.offer import Offer
from domain.interfaces.entity_interface import IEntity
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.country import Country
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
INTEGRATION_ENTITIES_COUNT = 2
UNSUPPORTED_ENTITY_ID = 123
MIXED_ENTITIES_COUNT = 4
MIXED_ENTITIES_VECTORIZED = 3
MIXED_ENTITIES_INVALID_ID = 999
SECOND_ENTITY_ID = 2


class UnsupportedEntity(IEntity):
    """Mock entity for testing unsupported source type."""

    def __init__(self, id: int):
        """Initialize with id."""
        self.id = id


def create_test_corps(entity_id: int = 1) -> Corps:
    """Create a test Corps entity for unit tests."""
    return Corps(
        code=f"CODE{entity_id}",
        category=Category.A,
        ministry=Ministry.MAA,
        diploma=Diploma(5),
        access_modalities=[AccessModality.CONCOURS_EXTERNE],
        label=Label(short_value="Test Corps", value="Test Corps Label"),
        processed_at=None,
        archived_at=None,
    )


def create_test_corps_for_integration(entity_id: int = 1) -> Corps:
    """Create a test Corps entity for integration tests."""
    return Corps(
        code=f"0000{entity_id + 2}",
        category=Category.A,
        ministry=Ministry.MAA if entity_id == 1 else Ministry.MESRI,
        diploma=Diploma(5 if entity_id == 1 else 7),
        access_modalities=[
            AccessModality.CONCOURS_EXTERNE,
            AccessModality.CONCOURS_INTERNE,
        ]
        if entity_id == 1
        else [AccessModality.CONCOURS_EXTERNE],
        label=Label(
            short_value="PROF LYCE PROF AGRI" if entity_id == 1 else "DIRE ETUD EHESS",
            value="Professeurs de lycée professionnel agricole"
            if entity_id == 1
            else "Directeurs d'études de l'Ecole",
        ),
        processed_at=None,
        archived_at=None,
    )


def create_test_concours(entity_id: int = 1) -> Concours:
    """Create a test Concours entity for unit tests."""
    return Concours(
        nor_original=NOR("AGRS2400001A"),
        nor_list=[NOR("AGRS2400001A")],
        category=Category.A,
        ministry=Ministry.MAA,
        access_modality=[AccessModality.CONCOURS_EXTERNE],
        corps="Test Corps",
        grade="Test Grade",
        written_exam_date=None,
        open_position_number=10,
        processed_at=None,
        archived_at=None,
    )


def create_test_concours_for_integration(entity_id: int = 1) -> Concours:
    """Create a test Concours entity for integration tests."""
    return Concours(
        nor_original=NOR(f"AGRS240000{entity_id}A"),
        nor_list=[NOR(f"AGRS240000{entity_id}A")],
        category=Category.A,
        ministry=Ministry.MAA if entity_id == 1 else Ministry.MESRI,
        access_modality=[AccessModality.CONCOURS_EXTERNE],
        corps=f"Test Corps {entity_id}",
        grade=f"Test Grade {entity_id}",
        written_exam_date=None,
        open_position_number=10 + entity_id,
        processed_at=None,
        archived_at=None,
    )


def create_test_offer(entity_id: int = 1) -> Offer:
    """Create a test Offer entity for unit tests."""
    return Offer(
        external_id=f"OFFER_{entity_id:03d}",
        verse=Verse.FPE,
        title="Développeur Python Senior",
        profile="Profil technique avec expertise Python",
        mission="Mission de développement",
        category=Category.A,
        contract_type=None,
        organization="Test Organization",
        offer_url=None,
        localisation=Localisation(
            country=Country("FRA"),
            region=Region(code="11"),
            department=Department(code="75"),
        ),
        publication_date=datetime(2024, 1, 15),
        beginning_date=LimitDate(datetime(2024, 12, 31)),
        processed_at=None,
        archived_at=None,
    )


def create_test_offer_for_integration(entity_id: int = 1) -> Offer:
    """Create a test Offer entity for integration tests."""
    return Offer(
        external_id=f"OFFER_{entity_id + 2:03d}",
        verse=Verse.FPE if entity_id == 1 else Verse.FPT,
        title=f"Développeur Python Senior {entity_id}",
        profile=f"Profil technique avec expertise Python {entity_id}",
        mission=f"Mission de développement {entity_id}",
        category=Category.A if entity_id == 1 else Category.B,
        contract_type=None,
        organization=f"Test Organization {entity_id}",
        offer_url=None,
        localisation=Localisation(
            country=Country("FRA"),
            region=Region(code="11" if entity_id == 1 else "84"),
            department=Department(code="75" if entity_id == 1 else "69"),
        ),
        publication_date=datetime(2024, 1, 15 + entity_id),
        beginning_date=LimitDate(datetime(2024, 12, 31)),
        processed_at=None,
        archived_at=None,
    )


def create_test_document(
    entity_id: int = 1, doc_type: DocumentType = DocumentType.GRADE
) -> Document:
    """Create a test Document entity."""
    return Document(
        external_id=f"test_doc_{entity_id}",
        raw_data={"content": f"Test document content {entity_id}"},
        type=doc_type,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
