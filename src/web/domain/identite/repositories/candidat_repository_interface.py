from typing import Protocol
from uuid import UUID

from ddd.base_repository_interface import IBaseRepository

from domain.identite.entities.candidat import Candidat
from domain.identite.entities.utilisateurs import Utilisateur


class ICandidatRepository(IBaseRepository[Candidat], Protocol):
    def create(self, utilisateur: Utilisateur, candidat: Candidat) -> Candidat: ...
    def get_by_email(self, email: str) -> Candidat | None: ...
    def get_by_ids(self, candidat_ids: list[UUID]) -> list[Candidat]: ...
