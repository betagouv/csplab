from typing import Protocol

from domain.identite.entities.candidat import Candidat
from domain.identite.entities.utilisateurs import Utilisateur


class ICandidatRepository(Protocol):
    def create(self, utilisateur: Utilisateur, candidat: Candidat) -> Candidat: ...
    def get_by_email(self, email: str) -> Candidat | None: ...
