"""Localisation value object."""

from dataclasses import dataclass

from domain.value_objects.department import Department
from domain.value_objects.region import Region


@dataclass(frozen=True)
class Localisation:
    """Localisation value object with region and department."""

    region: Region
    department: Department

    def __str__(self):
        """Return string representation."""
        return f"{self.region} - {self.department}"
