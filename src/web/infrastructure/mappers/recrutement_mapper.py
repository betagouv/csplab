from uuid import UUID

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
        etapes = tuple(
            EtapeRecrutement.build(
                entity_id=e.id,
                categorie=CategorieEtapeRecrutement(e.categorie),
                nom=e.nom,
            )
            for e in model.etapes.all()  # type: ignore[attr-defined]
        )
        responsables = tuple(
            UUID(str(liaison.agent_id))
            for liaison in model.responsables_liaisons.all()  # type: ignore[attr-defined]
        )
        return Recrutement.build(
            offre_id=model.offre_id,  # type: ignore[attr-defined]
            organisme_id=model.organisme_id,  # type: ignore[attr-defined]
            etapes=etapes,
            candidatures=(),
            responsables=responsables,
            status=StatutRecrutement.ACTIF,
        )
