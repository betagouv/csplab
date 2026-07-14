from typing import Protocol
from uuid import UUID

from ddd.base_repository_interface import IBaseRepository


class ICandidatureRepository(IBaseRepository, Protocol):
    def exists(self, candidature_id: UUID) -> bool: ...
    def exists_by_candidat_and_offre(
        self, candidat_id: UUID, offre_id: UUID
    ) -> bool: ...
