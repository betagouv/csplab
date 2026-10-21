from typing import NamedTuple
from uuid import UUID

from django.db.models import QuerySet

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.users.models import UserModel


class OrganismeDetails(NamedTuple):
    uuid: UUID
    nom: str
    authorized_actions: list[str]


class UtilisateurDetails(NamedTuple):
    utilisateur: UserModel
    # TODO(#1930): remove organisme_roles once the Vue front reads `organismes`
    organisme_roles: QuerySet[OrganismeAgentModel]
    authorized_actions: list[str]
    organismes: list[OrganismeDetails]


def get_utilisateur_details(*, utilisateur: UserModel) -> UtilisateurDetails:
    permissions = OrganismePermissionService()
    liaisons = (
        OrganismeAgentModel.objects.by_agent(utilisateur.username)
        .with_organisme()
        .order_by("organisme__nom", "organisme_id")
    )
    return UtilisateurDetails(
        utilisateur=utilisateur,
        organisme_roles=liaisons,
        authorized_actions=[
            action.value
            for action in permissions.actions_autorisees_utilisateur(utilisateur)
        ],
        organismes=[
            OrganismeDetails(
                uuid=liaison.organisme_id,
                nom=liaison.organisme.nom,
                authorized_actions=[
                    action.value
                    for action in permissions.actions_autorisees_organisme(
                        AgentOrganismeRole(liaison.role),
                        utilisateur=utilisateur,
                    )
                ],
            )
            for liaison in liaisons
        ],
    )
