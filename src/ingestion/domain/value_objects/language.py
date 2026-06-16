from dataclasses import dataclass

from domain.value_objects.niveau import Niveau


@dataclass(frozen=True)
class Language:
    iso_code: str
    niveau: Niveau
