from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import HttpUrl
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_kind import ContractKind
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.language import Language
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.offer_conditions import (
    JobVacancy,
    Management,
    WorkingPlace,
    WorkingTime,
)
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.verse import Verse


@dataclass
class Offer:
    reference: str
    source_id: UUID
    external_id: str
    title: str
    profile: str
    mission: str
    organization: str
    verse: Optional[Verse]
    category: Optional[Category]
    offer_nature: Optional[OfferNature]
    offer_url: Optional[HttpUrl]
    application_url: Optional[HttpUrl]
    localisation: Optional[Localisation]
    publication_date: datetime
    end_publication_date: Optional[datetime]
    beginning_date: Optional[LimitDate]
    application_deadline: Optional[datetime] = None
    contract_duration: Optional[str] = None
    employer_description: str = ""
    exercise_conditions: str = ""
    service_description: str = ""
    complements: str = ""
    contract_kind: Optional[ContractKind] = None
    education_level: Optional[int] = None
    experience: Optional[ExperienceLevel] = None
    diploma: Optional[str] = None
    languages: list[Language] = field(default_factory=list)
    specialisations: list[str] = field(default_factory=list)
    family_code: Optional[str] = None
    working_place: WorkingPlace = WorkingPlace.NON_DEFINI
    working_time: WorkingTime = WorkingTime.NON_DEFINI
    management: Optional[Management] = None
    job_vacancy: Optional[JobVacancy] = None
    talentsoft_organisme_entity_code: str = ""
    id: UUID = field(default_factory=uuid4)
