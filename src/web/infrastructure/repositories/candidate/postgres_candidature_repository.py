from uuid import UUID

from domain.candidate.entities.candidature import Candidature
from domain.candidate.exceptions.candidature_errors import CandidatureNexistePas
from domain.candidate.repositories.candidature_repository_interface import (
    ICandidatureRepository,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel


class PostgresCandidatureRepository(ICandidatureRepository):
    def get_by_offer(self, offer_id: UUID, candidate_id: UUID) -> Candidature:
        try:
            model = CandidatureModel.objects.get(  # type: ignore[attr-defined]
                offre_id=offer_id, candidat_id=candidate_id
            )
            return model.to_entity()
        except CandidatureModel.DoesNotExist as e:
            raise CandidatureNexistePas(candidate_id, offer_id) from e

    def save(self, candidature: Candidature) -> None:
        CandidatureModel.objects.update_or_create(  # type: ignore[attr-defined]
            candidat_id=candidature.candidat_id,
            offre_id=candidature.offre_id,
            defaults={
                "statut": candidature.statut.value,
                "documents": (
                    [str(d) for d in candidature.documents]
                    if candidature.documents
                    else None
                ),
                "soumise_le": candidature.soumise_le,
                "mise_a_jour_le": candidature.mise_a_jour_le,
            },
            create_defaults={"id": candidature.entity_id},
        )
