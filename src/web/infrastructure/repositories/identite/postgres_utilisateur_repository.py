from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.errors.identite_errors import (
    UtilisateurExisteDeja,
    UtilisateurNexistePas,
)
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)
from domain.identite.value_objects.organisme_role import OrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.users.models import UserModel


class PostgresUtilisateurRepository(IUtilisateurRepository):
    def get_by_username(
        self, username, with_organisme_roles: bool = False
    ) -> Utilisateur:
        try:
            utilisateur = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist as e:
            raise UtilisateurNexistePas(username) from e
        organisme_roles = (
            self._get_organisme_roles(username) if with_organisme_roles else None
        )
        return utilisateur.to_entity(organisme_roles=organisme_roles)

    def _get_organisme_roles(self, username) -> list[OrganismeRole]:
        liaisons = OrganismeAgentModel.objects.filter(agent_id=username).select_related(
            "organisme"
        )
        return [
            OrganismeRole(
                organisme_uuid=liaison.organisme_id,
                nom=liaison.organisme.nom,
                role=liaison.role,
            )
            for liaison in liaisons
        ]

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
