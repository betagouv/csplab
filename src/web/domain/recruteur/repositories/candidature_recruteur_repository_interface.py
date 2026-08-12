from typing import Protocol
from uuid import UUID

from ddd.base_repository_interface import IBaseRepository

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur


class ICandidatureRecruteurRepository(IBaseRepository, Protocol):
    def get_by_ids(self, ids: list[UUID]) -> list[CandidatureRecruteur]: ...
