from typing import List, Protocol
from uuid import UUID

from ddd.base_repository_interface import IBaseRepository
from referentiel.types import IBatchUpdate

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur
from domain.recruteur.errors.candidature_errors import CandidatureRecruteurError


class ICandidatureRecruteurRepository(IBaseRepository[CandidatureRecruteur], Protocol):
    def get_by_ids(self, ids: List[UUID]) -> List[CandidatureRecruteur]: ...
    def update_batch(
        self, candidatures: List[CandidatureRecruteur]
    ) -> IBatchUpdate[CandidatureRecruteur, CandidatureRecruteurError]: ...
