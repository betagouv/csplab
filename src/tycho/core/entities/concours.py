"""Corps entity for clean corps storage."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.ministry import Ministry


@dataclass
class Concours:
    """Concours entity."""

    id: int
    nor: str
    category: Category
    ministry: Ministry
    access_modality: AccessModality
    corps_id: int
    grade_id: int
    opening_registration_date: Optional[datetime]
    closing_registration_date: Optional[datetime]
    written_exam_date: datetime
    registration_url: Optional[str]
    open_position_number: int
