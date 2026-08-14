from datetime import datetime, timezone
from typing import List
from uuid import UUID

from referentiel.types import IBatchUpdate

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur
from domain.recruteur.errors.recrutement_errors import (
    CandidatureInexistante,
)
from domain.recruteur.repositories.candidature_recruteur_repository_interface import (
    ICandidatureRecruteurRepository,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.exceptions.exceptions import InfrastructureError
from infrastructure.mappers.candidature_recruteur_mapper import (
    CandidatureRecruteurMapper,
)


class PostgresCandidatureRecrutementRepository(ICandidatureRecruteurRepository):
    def __init__(self, mapper: CandidatureRecruteurMapper) -> None:
        self.mapper = mapper

    def get_by_id(self, candidature_id: UUID) -> CandidatureRecruteur:
        try:
            model = CandidatureModel.objects.get(id=candidature_id)
            return self.mapper.to_domain(model)
        except CandidatureModel.DoesNotExist as e:
            raise CandidatureInexistante(candidature_id) from e

    def get_by_ids(self, ids: List[UUID]) -> List[CandidatureRecruteur]:
        candidatures = list(
            CandidatureModel.objects.filter(id__in=ids)
            .select_for_update()  # protect from concurrency errors in usecase
            .select_related("candidat", "etape__recrutement__offre")
        )

        found_ids = {c.id for c in candidatures}
        missing_ids = [i for i in ids if i not in found_ids]
        if len(missing_ids) > 0:
            raise CandidatureInexistante(missing_ids[0])

        return [self.mapper.to_domain(c) for c in candidatures]

    def update_batch(
        self,
        candidatures: List[CandidatureRecruteur],
    ) -> IBatchUpdate[CandidatureRecruteur, InfrastructureError]:
        successes: List[CandidatureRecruteur] = []
        failures: List[tuple[UUID, InfrastructureError]] = []

        for candidature in candidatures:
            try:
                CandidatureModel.objects.filter(id=candidature.entity_id).update(
                    etape_id=candidature.etape_id,
                    updated_at=datetime.now(tz=timezone.utc),
                )
                successes.append(candidature)
            except Exception as e:
                failures.append((candidature.entity_id, InfrastructureError(str(e))))
        return {"successes": successes, "failures": failures}
