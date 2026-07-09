from uuid import UUID

from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper

from domain.candidate.entities.candidature import Candidature
from domain.candidate.value_objects.statut_candidature import StatutCandidature
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel


class CandidatureMapper(IFromDomainMapper, IToDomainMapper):
    def to_domain(self, model: CandidatureModel) -> Candidature:
        return Candidature.build(
            entity_id=model.id,
            candidat_id=UUID(model.candidat_id),  # type: ignore[arg-type]
            # recrutement.id == offre.id (PK partagée entre recrutement et offre)
            offre_id=model.etape.recrutement_id,
            statut=StatutCandidature(model.statut),
            documents=tuple(UUID(d) for d in model.documents)
            if model.documents
            else None,
            soumise_le=model.created_at,
            mise_a_jour_le=model.updated_at,
        )

    def from_domain(
        self, candidature: Candidature, etape_id: UUID
    ) -> "CandidatureModel":
        # La candidature ne connaît que l'offre ; l'étape courante (par défaut
        # l'étape ENTREE du recrutement correspondant) est résolue par
        # l'appelant (repository) et injectée ici via `etape_id`.
        return CandidatureModel(
            id=candidature.entity_id,
            candidat_id=str(candidature.candidat_id),  # UUID → VARCHAR(36)
            etape_id=etape_id,
            statut=candidature.statut.value,
            documents=[str(d) for d in candidature.documents]
            if candidature.documents
            else None,
        )
