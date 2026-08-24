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
from infrastructure.mappers.utilisateur_mapper import UtilisateurMapper


class PostgresUtilisateurRepository(IUtilisateurRepository):
    def __init__(self) -> None:
        self._mapper = UtilisateurMapper()

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
        return self._mapper.to_domain(utilisateur, organisme_roles=organisme_roles)

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
            return self._mapper.to_domain(UserModel.objects.get(email=email))
        except UserModel.DoesNotExist as e:
            raise UtilisateurNexistePas(email) from e

    def create(self, utilisateur: Utilisateur) -> Utilisateur:
        if UserModel.objects.filter(username=utilisateur.entity_id).exists():
            raise UtilisateurExisteDeja(utilisateur.entity_id)
        model = self._mapper.from_domain(utilisateur)
        model.set_unusable_password()
        model.save()
        return self._mapper.to_domain(model)
