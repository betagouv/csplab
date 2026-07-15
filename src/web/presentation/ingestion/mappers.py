from typing import Optional
from uuid import UUID

from ddd.mapper_interface import IToDomainMapper
from referentiel.entities.offer import Offer
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractKind, ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse


class LocalisationInputMapper(IToDomainMapper[dict, Localisation]):
    def to_domain(self, data: Optional[dict]) -> Optional[Localisation]:
        if not data:
            return None
        return Localisation(
            area=GeographicalArea(data["zone_geographique"]),
            country=Country(data["pays"]),
            region=Region(code=data["region"]),
            department=Department(code=data["departement"]),
            label=data.get("localisation_label") or None,
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
        )


class OfferInputMapper(IToDomainMapper[dict, Offer]):
    def __init__(self) -> None:
        self._localisation_mapper = LocalisationInputMapper()

    def to_domain(self, data: Optional[dict], source_id: UUID) -> Optional[Offer]:
        if not data:
            return None

        # todo handle multiple categories offers later
        category = (
            Category(sorted(data["categories"])[0]) if data.get("categories") else None
        )
        conditions = data.get("conditions") or None
        debut_contrat = conditions.get("debut_contrat") if conditions else None

        localisations = data.get("localisation", [])
        raw_localisation = localisations[0] if localisations else None

        forme_contrat = data.get("forme_contrat")

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
            source_id=source_id,
            long_title=data.get("titre_long") or None,
            application_url=data.get("url_candidature"),
            contract_kind=[ContractKind[name] for name in sorted(forme_contrat)]
            if forme_contrat
            else None,
            job_vacancy=data.get("vacance_poste") or None,
            employer=data["description"].get("employeur") or None,
            complements=data["description"].get("complements") or None,
            criteria=data.get("criteres") or None,
            conditions=conditions,
            contacts=list(data["contacts"]) if data.get("contacts") else None,
        )
