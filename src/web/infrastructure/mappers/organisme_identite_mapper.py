from uuid import UUID

from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper
from referentiel.entities.organisme import Organisme
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

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
            siret=SIRET(code=model.siret),
            parent_id=UUID(str(model.parent_id)) if model.parent_id else None,
            external_id=model.external_id,
            referentiel=model.referentiel,
            millesime=model.millesime,
            gestion_ats=model.gestion_ats,
            date_creation=model.created_at,
            date_derniere_activite=model.updated_at,
        )

    def from_domain(self, organisme: Organisme) -> OrganismeModel:
        return self.apply_to_model(OrganismeModel(id=organisme.entity_id), organisme)

    def apply_to_model(
        self, model: OrganismeModel, organisme: Organisme
    ) -> OrganismeModel:
        localisation_data = None
        if organisme.localisation:
            loc = organisme.localisation
            localisation_data = {
                "area": loc.area.value,
                "country": str(loc.country),
                "region": loc.region.code,
                "department": loc.department.code,
            }
        model.nom = organisme.nom
        model.versant = organisme.versant.value
        model.siret = organisme.siret.code
        model.parent_id = organisme.parent_id
        model.localisation = localisation_data
        model.external_id = organisme.external_id
        model.referentiel = organisme.referentiel
        model.millesime = organisme.millesime
        model.gestion_ats = organisme.gestion_ats
        model.date_creation = organisme.date_creation
        model.date_derniere_activite = organisme.date_derniere_activite
        return model
