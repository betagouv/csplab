"""French Region value object."""

from typing import ClassVar

from pydantic import BaseModel, field_validator


class Region(BaseModel):
    """French Region value object with INSEE code validation."""

    code: str

    # Valid French region INSEE codes
    VALID_CODES: ClassVar[set[str]] = {
        "11",  # Île-de-France
        "24",  # Centre-Val de Loire
        "27",  # Bourgogne-Franche-Comté
        "28",  # Normandie
        "32",  # Hauts-de-France
        "44",  # Grand Est
        "52",  # Pays de la Loire
        "53",  # Bretagne
        "75",  # Nouvelle-Aquitaine
        "76",  # Occitanie
        "84",  # Auvergne-Rhône-Alpes
        "93",  # Provence-Alpes-Côte d'Azur
        "94",  # Corse
        "01",  # Guadeloupe
        "02",  # Martinique
        "03",  # Guyane
        "04",  # La Réunion
        "06",  # Mayotte
        "DOM",  # Overseas regions placeholder
        "TOM",  # Overseas territories placeholder
    }

    @field_validator("code")
    @classmethod
    def validate_region_code(cls, v: str) -> str:
        """Validate French region INSEE code."""
        if v not in cls.VALID_CODES:
            raise ValueError(f"Invalid French region INSEE code: {v}")
        return v

    def __str__(self) -> str:
        """Return string representation."""
        return self.code
