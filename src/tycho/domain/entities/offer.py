"""Offer entity for job offers storage."""

from dataclasses import dataclass
from typing import Optional

from domain.interfaces.entity_interface import IEntity
from domain.value_objects.category import Category
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.verse import Verse


@dataclass
class Offer(IEntity):
    """Offer entity."""

    id: int
    external_id: str
    verse: Verse
    title: str
    profile: str
    category: Category
    localisation: Optional[Localisation]
    limit_date: Optional[LimitDate]
