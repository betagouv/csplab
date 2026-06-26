from uuid import UUID

from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.position_candidature import PositionCandidature
from domain.recruteur.value_objects.recrutement_status import RecrutementStatus
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel


class RecrutementMapper(IFromDomainMapper, IToDomainMapper):
    def to_domain(self, model: RecrutementModel) -> Recrutement:
        return Recrutement.build(
            entity_id=model.id,
            offre_id=model.offre_id,
            organisme_id=model.organisme_id,  # type: ignore[attr-defined]
            etapes=tuple(
                EtapeRecrutement.build(
                    entity_id=UUID(e["entity_id"]),
                    categorie=CategorieEtapeRecrutement(e["categorie"]),
                    nom=e["nom"],
                )
                for e in model.etapes
            ),
            status=RecrutementStatus(model.status),
            positions=tuple(
                PositionCandidature(
                    candidature_id=UUID(p["candidature_id"]),
                    etape_id=UUID(p["etape_id"]),
                    ordre=p.get("ordre"),
                )
                for p in model.positions
            ),
            responsables_ids=tuple(UUID(uid) for uid in model.responsables_ids),
            derniere_activite_le=model.updated_at,
            candidat_recrute_id=(
                UUID(raw)
                if (raw := model.candidat_recrute_id)  # type: ignore[attr-defined]
                else None
            ),
        )

    def from_domain(self, entity: Recrutement) -> RecrutementModel:
        return RecrutementModel(
            id=entity.entity_id,
            offre_id=entity.offre_id,
            organisme_id=entity.organisme_id,
            status=entity.status.value,
            etapes=[
                {
                    "entity_id": str(e.entity_id),
                    "categorie": e.categorie.value,
                    "nom": e.nom,
                }
                for e in entity.etapes
            ],
            positions=[
                {
                    "candidature_id": str(p.candidature_id),
                    "etape_id": str(p.etape_id),
                    "ordre": p.ordre,
                }
                for p in entity.positions
            ],
            responsables_ids=[str(uid) for uid in entity.responsables_ids],
            candidat_recrute_id=(
                str(entity.candidat_recrute_id) if entity.candidat_recrute_id else None
            ),
        )
