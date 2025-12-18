"""Offer entity for job offers storage."""

from dataclasses import dataclass
from typing import Optional

from core.interfaces.entity_interface import IEntity
from core.value_objects.category import Category
from core.value_objects.limit_date import LimitDate
from core.value_objects.localisation import Localisation
from core.value_objects.verse import Verse


@dataclass
class Offer(IEntity):
    """Offer entity."""

    id: int
    external_id: str
    verse: Verse
    titre: str
    profile: str
    category: Category
    localisation: Optional[Localisation]
    limit_date: Optional[LimitDate]
