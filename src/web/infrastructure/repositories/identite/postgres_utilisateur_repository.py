from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.errors.identite_errors import (
    UtilisateurExisteDeja,
    UtilisateurNexistePas,
)
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)
from infrastructure.django_apps.users.models import UserModel


class PostgresUtilisateurRepository(IUtilisateurRepository):
    def get_by_username(self, username) -> Utilisateur:
        try:
            utilisateur = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist as e:
            raise UtilisateurNexistePas(username) from e
        return utilisateur.to_entity()

    def get_by_email(self, email: str) -> Utilisateur:
        try:
            return UserModel.objects.get(email=email).to_entity()
        except UserModel.DoesNotExist as e:
            raise UtilisateurNexistePas(email) from e

    def create(self, utilisateur: Utilisateur) -> Utilisateur:
        if UserModel.objects.filter(username=utilisateur.entity_id).exists():
            raise UtilisateurExisteDeja(utilisateur.entity_id)
        model = UserModel.from_entity(utilisateur)
        model.set_unusable_password()
        model.save()
        return model.to_entity()
