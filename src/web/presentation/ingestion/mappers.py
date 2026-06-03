from typing import Optional
from uuid import UUID

from ddd.mapper_interface import IToDomainMapper

from domain.entities.offer import Offer
from domain.value_objects.area import GeographicalArea
from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
from domain.value_objects.country import Country
from domain.value_objects.department import Department
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.region import Region
from domain.value_objects.verse import Verse


class LocalisationInputMapper(IToDomainMapper[dict, Localisation]):
    def to_domain(self, data: Optional[dict]) -> Optional[Localisation]:
        if not data:
            return None
        return Localisation(
            area=GeographicalArea(data["zone_geographique"]),
            country=Country(data["pays"]),
            region=Region(code=data["region"]),
            department=Department(code=data["departement"]),
        )


class OfferInputMapper(IToDomainMapper[dict, Offer]):
    def __init__(self) -> None:
        self._localisation_mapper = LocalisationInputMapper()

    def to_domain(self, data: Optional[dict]) -> Optional[Offer]:
        if not data:
            return None

        # todo handle multiple categories offers later
        category = (
            Category(sorted(data["categories"])[0]) if data.get("categories") else None
        )
        conditions = data.get("conditions", {})
        debut_contrat = conditions.get("debut_contrat") if conditions else None

        localisations = data.get("localisation", [])
        raw_localisation = localisations[0] if localisations else None

        return Offer(
            external_id=f"{data['identification']['versant']}-{data['identification']['reference']}",
            reference=data["identification"]["reference"],
            title=data["titre"],
            profile=data["description"]["profil"],
            mission=data["description"]["mission"],
            organization=data["organisation"]["nom"],
            publication_date=data["publication"]["debut_publication"],
            verse=Verse(data["identification"]["versant"]),
            category=category,
            contract_type=ContractType(data["type_contrat"]),
            offer_url=data.get("url_offre"),
            localisation=self._localisation_mapper.to_domain(raw_localisation),
            beginning_date=LimitDate(debut_contrat) if debut_contrat else None,
            family_code=data["profession"]["metier"],
            source_id=UUID(data["identification"]["source"]),
        )
