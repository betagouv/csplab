"""Localisation value object."""

from dataclasses import dataclass

from domain.value_objects.country import Country
from domain.value_objects.department import Department
from domain.value_objects.region import Region


@dataclass(frozen=True)
class Localisation:
    """Localisation value object with region and department."""

    region: Region
    department: Department
    country: Country

    def __str__(self):
        """Return string representation."""
        return (
            f"{self.country.short_name} - {self.region.code} - {self.department.code}"
        )
