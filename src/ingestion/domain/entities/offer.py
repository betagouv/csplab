from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import HttpUrl

from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
from domain.value_objects.experience import Experience
from domain.value_objects.language import Language
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.verse import Verse


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
    contract_type: Optional[ContractType]
    offer_url: Optional[HttpUrl]
    application_url: Optional[HttpUrl]
    localisation: Optional[Localisation]
    publication_date: datetime
    end_publication_date: Optional[datetime]
    beginning_date: Optional[LimitDate]
    education_level: Optional[int] = None
    experience: Optional[Experience] = None
    diploma: Optional[str] = None
    languages: list[Language] = field(default_factory=list)
    specialisations: list[str] = field(default_factory=list)
    family_code: Optional[str] = None
    id: UUID = field(default_factory=uuid4)
