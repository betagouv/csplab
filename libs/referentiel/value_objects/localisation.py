from dataclasses import dataclass
from typing import Optional

from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.departement_region import (
    region_et_zone_pour_departement,
)
from referentiel.value_objects.department import Department
from referentiel.value_objects.region import Region

# TODO : Redefine Localisation as follow
# - geographical_area: GeographicalArea
# - country: Country
# - coordinates: Coordinates
# - city: Optional[str]
# - subdivision: Optional[Subdivision] #for France only


FRANCE = Country("FRA")


@dataclass(frozen=True)
class Localisation:
    area: GeographicalArea
    country: Country
    # Region and department subdivide France only: both are set for FRA, both
    # are None for any other country.
    region: Optional[Region]
    department: Optional[Department]
    label: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    def __post_init__(self) -> None:
        has_subdivision = (self.region is not None, self.department is not None)
        if self.is_in_france and has_subdivision != (True, True):
            raise ValueError("A localisation in France needs a region and a department")
        if not self.is_in_france and has_subdivision != (False, False):
            raise ValueError(
                f"A localisation in {self.country} cannot have a region nor a "
                "department"
            )

    @property
    def is_in_france(self) -> bool:
        return self.country == FRANCE

    def __str__(self):
        if self.region is None or self.department is None:
            return self.country.short_name
        return (
            f"{self.country.short_name} - {self.region.code} - {self.department.code}"
        )

    @classmethod
    def from_department(
        cls,
        department: Department,
        *,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ) -> Optional["Localisation"]:
        region_et_zone = region_et_zone_pour_departement(department)
        if region_et_zone is None:
            return None

        region, area = region_et_zone
        return cls(
            area=area,
            country=FRANCE,
            region=region,
            department=department,
            latitude=latitude,
            longitude=longitude,
        )
