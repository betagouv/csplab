from uuid import UUID

from django.db import IntegrityError
from referentiel.exceptions.offer_errors import OfferDoesNotExist

from domain.candidate.entities.candidature import CandidatureCandidat
from domain.candidate.exceptions.candidature_errors import CandidatureNexistePas
from domain.candidate.repositories.candidature_repository_interface import (
    ICandidatureRepository,
)
from domain.identite.exceptions.candidat_errors import CandidatInexistant
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.mappers.candidature_mappers import CandidatureCandidatMapper


class PostgresCandidatureRepository(ICandidatureRepository):
    def __init__(self) -> None:
        self._mapper = CandidatureCandidatMapper()

    def get_by_offer(self, offer_id: UUID, candidate_id: UUID) -> CandidatureCandidat:
        try:
            model = CandidatureModel.objects.get(  # type: ignore[attr-defined]
                offre_id=offer_id,
                candidat_id=str(candidate_id),  # type: ignore[misc]  # FK to_field=utilisateur_id (VARCHAR)
            )
            return self._mapper.to_domain(model)
        except CandidatureModel.DoesNotExist as e:
            raise CandidatureNexistePas(candidate_id, offer_id) from e

    def save(self, candidature: CandidatureCandidat) -> None:
        try:
            CandidatureModel.objects.update_or_create(  # type: ignore[attr-defined]
                candidat_id=str(candidature.candidat_id),  # type: ignore[misc]  # UUID → VARCHAR(36)
                offre_id=candidature.offre_id,
                defaults={
                    "statut": candidature.statut.value,
                    "documents": (
                        [str(d) for d in candidature.documents]
                        if candidature.documents
                        else None
                    ),
                },
                create_defaults={"id": candidature.entity_id},
            )
        except IntegrityError as e:
            # SQLSTATE 23503: foreign key constraint violation
            # PostgreSQL error message contains the column name involved
            error_detail = str(e)
            if "candidat_id" in error_detail:
                raise CandidatInexistant(candidature.candidat_id) from e
            if "offre_id" in error_detail:
                raise OfferDoesNotExist(candidature.offre_id) from e
            raise
