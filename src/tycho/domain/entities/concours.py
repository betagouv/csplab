"""Concours entity for clean concours storage."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from domain.interfaces.entity_interface import IEntity
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.ministry import Ministry
from domain.value_objects.nor import NOR


@dataclass
class Concours(IEntity):
    """Concours entity."""

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
    processing: bool = False
    processed_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None
    id: UUID = field(default_factory=uuid4)
