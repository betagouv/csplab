from dataclasses import dataclass

from referentiel.value_objects.language_level import LanguageLevel


@dataclass(frozen=True)
class Language:
    iso_code: str
    language_level: LanguageLevel
