from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper

from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_role import OrganismeRole
from infrastructure.django_apps.users.models import UserModel


class UtilisateurMapper(
    IFromDomainMapper[Utilisateur, UserModel],
    IToDomainMapper[UserModel, Utilisateur],
):
    def to_domain(
        self, model: UserModel, organisme_roles: list[OrganismeRole] | None = None
    ) -> Utilisateur:
        return Utilisateur(
            entity_id=model.username,
            email=model.email,
            prenom=model.first_name,
            nom=model.last_name,
            is_superuser=model.is_superuser,
            organisme_roles=organisme_roles or [],
        )

    def from_domain(self, utilisateur: Utilisateur) -> UserModel:
        return UserModel(
            username=utilisateur.entity_id,
            email=utilisateur.email,
            first_name=utilisateur.prenom,
            last_name=utilisateur.nom,
            is_superuser=utilisateur.is_superuser,
        )
