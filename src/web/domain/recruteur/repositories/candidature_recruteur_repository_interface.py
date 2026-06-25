from typing import Protocol
from uuid import UUID

from ddd.base_repository_interface import IBaseRepository

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur


class ICandidatureRecruteurRepository(
    IBaseRepository[CandidatureRecruteur], Protocol
):
    def list_by_offre(self, offre_id: UUID) -> list[CandidatureRecruteur]: ...
