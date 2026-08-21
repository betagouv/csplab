from uuid import UUID

from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)


class GetUtilisateurDetailUsecase:
    def __init__(self, utilisateur_repository: IUtilisateurRepository):
        self.utilisateur_repository = utilisateur_repository

    def execute(self, username: UUID) -> Utilisateur:
        return self.utilisateur_repository.get_by_username(
            username, with_organisme_roles=True
        )
