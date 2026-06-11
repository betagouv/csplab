from uuid import UUID

from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)


class GetUtilisateurDetailUsecase:
    def __init__(self, utilisateur_repository: IUtilisateurRepository):
        self.utilisateur_repository = utilisateur_repository

    def execute(self, entity_id: UUID) -> Utilisateur:
        return self.utilisateur_repository.get_by_entity_id(entity_id)
