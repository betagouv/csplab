from uuid import UUID

from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from domain.identite.entities.organisme import Organisme
from domain.identite.value_objects.siret import SIRET
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel


class OrganismeIdentiteMapper(IFromDomainMapper, IToDomainMapper):
    def to_domain(self, model: OrganismeModel) -> Organisme:
        localisation: Localisation | None = None
        if model.localisation:
            loc = model.localisation
            localisation = Localisation(
                area=GeographicalArea(loc["area"]),
                country=Country(loc["country"]),
                region=Region(code=loc["region"]),
                department=Department(code=loc["department"]),
            )
        return Organisme.build(
            entity_id=UUID(str(model.id)),
            nom=model.nom,
            versant=Verse(model.versant),
            localisation=localisation,
            siret=SIRET(model.siret),
            parent_id=UUID(str(model.parent_id)) if model.parent_id else None,
        )

    def from_domain(self, organisme: Organisme) -> OrganismeModel:
        localisation_data = None
        if organisme.localisation:
            loc = organisme.localisation
            localisation_data = {
                "area": loc.area.value,
                "country": str(loc.country),
                "region": loc.region.code,
                "department": loc.department.code,
            }
        return OrganismeModel(
            id=organisme.entity_id,
            nom=organisme.nom,
            versant=organisme.versant.value,
            siret=organisme.siret.value,
            parent_id=organisme.parent_id,
            localisation=localisation_data,
        )
