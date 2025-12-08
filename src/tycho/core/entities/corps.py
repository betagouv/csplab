"""Corps entity for clean corps storage."""

from dataclasses import dataclass
from typing import List, Optional

from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.diploma import Diploma
from core.value_objects.label import Label
from core.value_objects.ministry import Ministry


@dataclass
class Corps:
    """Corps entity."""

    id: int
    code: str
    category: Optional[Category]
    ministry: Ministry
    diploma: Optional[Diploma]
    access_modalities: List[AccessModality]
    label: Label
