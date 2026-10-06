from dataclasses import dataclass
from typing import List, Optional

from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.offer_conditions import Management, WorkingPlace
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse


@dataclass
class GetFilteredOffersInput:
    active: bool
    category: Optional[List[Category]] = None
    verse: Optional[List[Verse]] = None
    offer_nature: Optional[List[OfferNature]] = None
    experience_level: Optional[List[ExperienceLevel]] = None
    management: Optional[List[Management]] = None
    working_place: Optional[List[WorkingPlace]] = None
    region: Optional[List[Region]] = None
    department: Optional[List[Department]] = None
    country: Optional[List[Country]] = None
    area: Optional[List[GeographicalArea]] = None
    domain: Optional[List[str]] = None
    organization: Optional[List[str]] = None
    published_within_days: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_km: Optional[int] = None
    keywords: Optional[str] = None
