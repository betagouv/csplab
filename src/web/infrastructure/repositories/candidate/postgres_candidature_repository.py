from uuid import UUID

from django.db import IntegrityError

from domain.candidate.entities.candidature import Candidature
from domain.candidate.repositories.candidature_repository_interface import (
    ICandidatureRepository,
)
from domain.identite.exceptions.candidat_errors import CandidatInexistant
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.mappers.candidature_mapper import CandidatureMapper


class PostgresCandidatureRepository(ICandidatureRepository):
    def __init__(self, mapper: CandidatureMapper) -> None:
        self.mapper = mapper

    def exists(self, candidature_id: UUID) -> bool:
        return CandidatureModel.objects.filter(  # type: ignore[attr-defined]
            id=candidature_id
        ).exists()

    def save(self, candidature: Candidature) -> None:
        try:
            CandidatureModel.objects.update_or_create(  # type: ignore[attr-defined]
                id=candidature.entity_id,
                defaults={
                    "statut": candidature.statut.value,
                    "documents": (
                        [str(d) for d in candidature.documents]
                        if candidature.documents
                        else None
                    ),
                },
                create_defaults={
                    "id": candidature.entity_id,
                    "candidat_id": str(candidature.candidat_id),  # type: ignore[misc]  # UUID → VARCHAR(36)
                    "statut": candidature.statut.value,
                    "documents": (
                        [str(d) for d in candidature.documents]
                        if candidature.documents
                        else None
                    ),
                    "etape_id": EtapeModel.objects.filter(
                        recrutement_id=candidature.offre_id,
                        categorie=CategorieEtapeRecrutement.ENTREE.value,
                    )
                    .values_list("id", flat=True)
                    .first(),
                },
            )
        except IntegrityError as e:
            error_detail = str(e)
            if "candidat_id" in error_detail:
                raise CandidatInexistant(candidature.candidat_id) from e
            raise
