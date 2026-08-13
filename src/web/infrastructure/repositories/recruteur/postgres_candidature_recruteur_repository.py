from typing import List
from uuid import UUID

from django.db import transaction
from referentiel.types import IBatchUpdate

from domain.candidate.entities.candidature import Candidature
from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur
from domain.recruteur.errors.candidature_errors import (
    CandidatureInexistante,
    CandidatureRecruteurError,
)
from domain.recruteur.repositories.candidature_recruteur_repository_interface import (
    ICandidatureRecruteurRepository,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.mappers.candidature_recruteur_mapper import (
    CandidatureRecruteurMapper,
)


class PostgresCandidatureRecrutementRepository(ICandidatureRecruteurRepository):
    def __init__(self, mapper: CandidatureRecruteurMapper) -> None:
        self.mapper = mapper

    def get_by_ids(
        self, ids: List[UUID]
    ) -> List[tuple[Candidature, CandidatureRecruteur]]:
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

    def upsert_batch(
        self,
        candidatures: List[tuple[Candidature, CandidatureRecruteur]],
    ) -> IBatchUpdate[CandidatureRecruteur, CandidatureRecruteurError]:
        successes: List[CandidatureRecruteur] = []
        failures: List[tuple[UUID, CandidatureRecruteurError]] = []

        with transaction.atomic():  # protect from concurrency errors
            for entities in candidatures:
                _, candidature_recruteur = entities
                sp = transaction.savepoint()
                try:
                    model = self.mapper.from_domain(entities)
                    model.save()
                    successes.append(candidature_recruteur)
                except Exception as e:
                    transaction.savepoint_rollback(
                        sp
                    )  # avoid global rollback if error on one item and save error
                    failures.append(
                        (
                            candidature_recruteur.entity_id,
                            CandidatureRecruteurError(str(e)),
                        )
                    )

        return {"successes": successes, "failures": failures}
