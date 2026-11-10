from typing import NamedTuple
from uuid import UUID

from django.db.models import QuerySet

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
)
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


def get_user_info(*, utilisateur: UserModel) -> UtilisateurDetails:
    permissions = OrganismePermissionService()
    liaisons = (
        OrganismeAgentModel.objects.by_agent(utilisateur.username)
        .with_organisme()
        .order_by("organisme__nom", "organisme_id")
    )
    organisme_ids_responsable = {
        liaison.recrutement.organisme_id
        for liaison in RecrutementAgentModel.objects.organisme_as_responsable(
            utilisateur.username
        )
    }
    return UtilisateurDetails(
        utilisateur=utilisateur,
        organisme_roles=liaisons,
        authorized_actions=[
            action.value for action in permissions.authorized_actions_user(utilisateur)
        ],
        organismes=[
            OrganismeDetails(
                uuid=liaison.organisme_id,
                nom=liaison.organisme.nom,
                authorized_actions=[
                    action.value
                    for action in permissions.authorized_actions_organisme(
                        AgentOrganismeRole(liaison.role),
                        utilisateur=utilisateur,
                        organisme_id=liaison.organisme_id,
                        organisme_ids_responsable=organisme_ids_responsable,
                    )
                ],
            )
            for liaison in liaisons
        ],
    )
