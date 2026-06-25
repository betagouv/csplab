from uuid import UUID

from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper

from domain.candidate.entities.candidature import CandidatureCandidat
from domain.candidate.value_objects.statut_candidature import StatutCandidature
from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel


class CandidatureCandidatMapper(IFromDomainMapper, IToDomainMapper):
    def to_domain(self, model: CandidatureModel) -> CandidatureCandidat:
        return CandidatureCandidat.build(
            entity_id=model.id,
            candidat_id=UUID(model.candidat_id),  # type: ignore[arg-type]
            offre_id=model.offre_id,  # type: ignore[attr-defined]
            statut=StatutCandidature(model.statut),
            documents=tuple(UUID(d) for d in model.documents)
            if model.documents
            else None,
            soumise_le=model.created_at,
            mise_a_jour_le=model.updated_at,
        )

    def from_domain(self, candidature: CandidatureCandidat) -> CandidatureModel:
        return CandidatureModel(
            id=candidature.entity_id,
            candidat_id=str(candidature.candidat_id),  # UUID → VARCHAR(36)
            offre_id=candidature.offre_id,
            statut=candidature.statut.value,
            documents=[str(d) for d in candidature.documents]
            if candidature.documents
            else None,
        )


class CandidatureRecruteurMapper(IToDomainMapper):
    def to_domain(self, model: CandidatureModel) -> CandidatureRecruteur:
        return CandidatureRecruteur.build(
            entity_id=model.id,
            candidat_id=UUID(model.candidat_id),  # type: ignore[arg-type]
            offre_id=model.offre_id,  # type: ignore[attr-defined]
            documents=tuple(UUID(d) for d in model.documents)
            if model.documents
            else None,
            soumise_le=model.created_at,
            mise_a_jour_le=model.updated_at,
        )
