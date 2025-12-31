"""Corps entity for clean corps storage."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from core.interfaces.entity_interface import IEntity
from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.ministry import Ministry
from core.value_objects.nor import NOR


@dataclass
class Concours(IEntity):
    """Concours entity."""

    id: int
    nor_original: NOR
    nor_list: List[NOR]
    category: Category
    ministry: Ministry
    access_modality: List[AccessModality]
    corps: str
    grade: str
    # opening_registration_date: Optional[datetime]
    # closing_registration_date: Optional[datetime]
    written_exam_date: Optional[datetime]
    # registration_url: Optional[str]
    open_position_number: int
