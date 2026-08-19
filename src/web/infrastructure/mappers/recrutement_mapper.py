from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.statut_recrutement import StatutRecrutement
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel


class RecrutementMapper(IFromDomainMapper, IToDomainMapper):
    def to_domain(self, model: RecrutementModel) -> Recrutement:
        etapes = []
        candidatures = []
        for e in model.etapes.all():  # type: ignore[attr-defined]
            candidatures_etapes = [
                c.id
                for c in e.candidatures.all()  # type: ignore[attr-defined]
            ]
            candidatures.extend(candidatures_etapes)
            etapes.append(
                EtapeRecrutement.build(
                    entity_id=e.id,
                    categorie=CategorieEtapeRecrutement(e.categorie),
                    nom=e.nom,
                    candidatures=candidatures_etapes or None,
                )
            )
        agents = tuple(
            liaison.agent_id
            for liaison in model.agents_liaisons.all()  # type: ignore[attr-defined]
        )
        return Recrutement.build(
            offre_id=model.offre_id,  # type: ignore[attr-defined]
            organisme_id=model.organisme_id,  # type: ignore[attr-defined]
            etapes=tuple(etapes),
            candidatures=tuple(candidatures),
            agents=agents,
            status=StatutRecrutement.ACTIF,
            derniere_activite_le=model.updated_at,
        )

    def from_domain(self, etapes: tuple[EtapeRecrutement, ...]) -> list[dict]:
        return [
            {
                "entity_id": str(etape.entity_id),
                "categorie": etape.categorie.value,
                "nom": etape.nom,
            }
            for etape in etapes
        ]
