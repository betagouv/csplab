from uuid import UUID

from ddd.mapper_interface import IToDomainMapper

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel


class CandidatureRecruteurMapper(
    IToDomainMapper[CandidatureModel, CandidatureRecruteur],
):
    def to_domain(self, model: CandidatureModel) -> CandidatureRecruteur:
        return CandidatureRecruteur.build(
            entity_id=model.id,
            candidat_id=UUID(model.candidat_id),
            recrutement_id=model.etape.recrutement.offre_id,
            etape_id=model.etape_id,
            derniere_activite_le=model.updated_by_recruteur or model.updated_at,
        )
