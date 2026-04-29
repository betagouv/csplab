from datetime import datetime, timezone

from domain.entities.concours import Concours
from domain.entities.corps import Corps
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
    def __init__(self, id: int):
        self.id = id


def create_test_corps(entity_id: int = 1) -> Corps:
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


def create_test_concours(entity_id: int = 1) -> Concours:
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


def create_test_offer(entity_id: int = 1) -> Offer:
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
        publication_date=datetime(2024, 1, 15, tzinfo=timezone.utc),
        beginning_date=LimitDate(datetime(2024, 12, 31, tzinfo=timezone.utc)),
        processed_at=None,
        archived_at=None,
    )
