from referentiel.exceptions.identite_errors import UtilisateurDoesNotExist

from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)
from infrastructure.django_apps.users.models import UserModel


class PostgresUtilisateurRepository(IUtilisateurRepository):
    def get_by_entity_id(self, entity_id) -> Utilisateur:
        try:
            utilisateur = UserModel.objects.get(username=entity_id)
        except UserModel.DoesNotExist as e:
            raise UtilisateurDoesNotExist(entity_id) from e
        return utilisateur.to_entity()
