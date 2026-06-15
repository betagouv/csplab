from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import HttpUrl

from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
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
    localisation: Optional[Localisation]
    publication_date: datetime
    beginning_date: Optional[LimitDate]
    family_code: Optional[str] = None
    id: UUID = field(default_factory=uuid4)
