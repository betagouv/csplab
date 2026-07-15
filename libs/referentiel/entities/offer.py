from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ddd.entity_interface import IEntity
from pydantic import HttpUrl

from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractKind
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.verse import Verse


@dataclass
class Offer(IEntity):
    external_id: str
    title: str
    profile: str
    mission: str
    organization: str
    verse: Optional[Verse]
    category: Optional[Category]
    contract_type: Optional[ContractType]
    contract_kind: Optional[ContractKind]
    offer_url: Optional[HttpUrl]
    localisation: Optional[Localisation]
    publication_date: datetime
    beginning_date: Optional[LimitDate]
    reference: str
    family_code: Optional[str] = None
    long_title: Optional[str] = None
    application_url: Optional[HttpUrl] = None
    contract_kind: Optional[list[str]] = None
    job_vacancy: Optional[str] = None
    employer: Optional[str] = None
    complements: Optional[str] = None
    criteria: Optional[dict] = None
    conditions: Optional[dict] = None
    contacts: Optional[list[dict]] = None
    source_id: UUID = field(default_factory=uuid4)
    processing: bool = False
    processed_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None
    id: UUID = field(default_factory=uuid4)
