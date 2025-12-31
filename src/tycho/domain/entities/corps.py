"""Corps entity for clean corps storage."""

from dataclasses import dataclass
from typing import List, Optional

from core.interfaces.entity_interface import IEntity
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.diploma import Diploma
from domain.value_objects.label import Label
from domain.value_objects.ministry import Ministry


@dataclass
class Corps(IEntity):
    """Corps entity."""

    id: int
    code: str
    category: Optional[Category]
    ministry: Ministry
    diploma: Optional[Diploma]
    access_modalities: List[AccessModality]
    label: Label
