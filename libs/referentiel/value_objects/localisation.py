from dataclasses import dataclass

from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.region import Region

# TODO : Redefine Localisation as follow
# - geographical_area: GeographicalArea
# - country: Country
# - coordinates: Coordinates
# - city: Optional[str]
# - subdivision: Optional[Subdivision] #for France only


@dataclass(frozen=True)
class Localisation:
    area: GeographicalArea
    country: Country
    region: Region
    department: Department

    def __str__(self):
        return (
            f"{self.country.short_name} - {self.region.code} - {self.department.code}"
        )
