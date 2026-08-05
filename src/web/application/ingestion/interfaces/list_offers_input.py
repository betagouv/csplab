from dataclasses import dataclass
from typing import List, Optional

from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.offer_conditions import Management, WorkingPlace
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse


@dataclass
class GetFilteredOffersInput:
    active: bool
    external_id_contains: Optional[str]
    category: Optional[List[Category]] = None
    verse: Optional[List[Verse]] = None
    contract_type: Optional[List[ContractType]] = None
    experience_level: Optional[List[ExperienceLevel]] = None
    management: Optional[List[Management]] = None
    working_place: Optional[List[WorkingPlace]] = None
    region: Optional[List[Region]] = None
    department: Optional[List[Department]] = None
    country: Optional[List[Country]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_km: Optional[int] = None
