from typing import Protocol
from uuid import UUID

from ddd.base_repository_interface import IBaseRepository

from domain.candidate.entities.candidature import Candidature


class ICandidatureRepository(IBaseRepository[Candidature], Protocol):
    def exists_by_candidat_and_offre(
        self, candidat_id: UUID, offre_id: UUID
    ) -> bool: ...
