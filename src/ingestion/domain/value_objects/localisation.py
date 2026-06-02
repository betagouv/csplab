from dataclasses import dataclass

from domain.value_objects.area import GeographicalArea
from domain.value_objects.country import Country
from domain.value_objects.department import Department
from domain.value_objects.region import Region


@dataclass(frozen=True)
class Localisation:
    area: GeographicalArea
    country: Country
    region: Region
    department: Department

    def __str__(self):
        return f"{self.country} - {self.region.code} - {self.department.code}"
