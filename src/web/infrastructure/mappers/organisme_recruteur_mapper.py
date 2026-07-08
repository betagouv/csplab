from uuid import UUID

from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel


class OrganismeRecruteurMapper(IFromDomainMapper, IToDomainMapper):
    def to_domain(self, model: OrganismeModel) -> OrganismeRecruteur:
        etapes: tuple[EtapeRecrutement, ...] | None = None
        if model.etapes is not None:
            etapes = tuple(
                EtapeRecrutement.build(
                    entity_id=UUID(item["entity_id"]),
                    categorie=CategorieEtapeRecrutement(item["categorie"]),
                    nom=item["nom"],
                )
                for item in model.etapes
            )
        return OrganismeRecruteur.build(entity_id=model.id, etapes=etapes)

    def from_domain(self, etapes: tuple[EtapeRecrutement, ...]) -> list[dict]:
        return [
            {
                "entity_id": str(etape.entity_id),
                "categorie": etape.categorie.value,
                "nom": etape.nom,
            }
            for etape in etapes
        ]
