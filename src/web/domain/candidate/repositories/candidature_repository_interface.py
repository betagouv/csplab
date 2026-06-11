from typing import Protocol
from uuid import UUID

from ddd.base_repository_interface import IBaseRepository

from domain.candidate.entities.candidature import Candidature


class ICandidatureRepository(IBaseRepository, Protocol):
    def get_by_offer(self, offer_id: UUID, candidate_id: UUID) -> Candidature: ...
