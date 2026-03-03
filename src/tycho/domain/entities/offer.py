"""Offer entity for job offers storage."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import HttpUrl

from domain.interfaces.entity_interface import IEntity
from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.verse import Verse


@dataclass
class Offer(IEntity):
    """Offer entity."""

    external_id: str
    verse: Optional[Verse]
    title: str
    profile: str
    mission: str
    category: Optional[Category]
    contract_type: Optional[ContractType]
    organization: str
    offer_url: Optional[HttpUrl]
    localisation: Optional[Localisation]
    publication_date: datetime
    beginning_date: Optional[LimitDate]
    processing: bool = False
    processed_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None
    id: UUID = field(default_factory=uuid4)
