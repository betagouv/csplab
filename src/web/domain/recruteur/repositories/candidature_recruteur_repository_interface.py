from typing import List, Protocol
from uuid import UUID

from ddd.base_repository_interface import IBaseRepository
from referentiel.types import IBatchUpdate

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur
from domain.recruteur.errors.recrutement_errors import RecrutementError


class ICandidatureRecruteurRepository(IBaseRepository[CandidatureRecruteur], Protocol):
    def get_by_ids(self, ids: List[UUID]) -> List[CandidatureRecruteur]: ...
    def update_batch(
        self, candidatures: List[CandidatureRecruteur]
    ) -> IBatchUpdate[CandidatureRecruteur, RecrutementError]: ...
