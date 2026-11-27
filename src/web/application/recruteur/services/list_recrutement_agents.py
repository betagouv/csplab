from collections.abc import Iterable
from uuid import UUID

from django.db.models import QuerySet

from application.identite.context_services.permission_service import (
    PermissionService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.identite.value_objects.permission_action import PermissionAction
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
)
from infrastructure.django_apps.users.models import UserModel


def list_recrutement_agents(
    *, organisme_id: UUID, recrutement_id: UUID, utilisateur: UserModel
) -> QuerySet[RecrutementAgentModel]:
    PermissionService().authorize(
        action=PermissionAction.LIST_RECRUTEMENT_AGENTS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )

    contexte = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    contexte.check_recrutement_belongs_to_organisme()

    return RecrutementAgentModel.objects.by_recrutement(recrutement_id).with_tags()


def with_authorized_actions(
    members: Iterable[RecrutementAgentModel],
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    utilisateur: UserModel,
) -> list[RecrutementAgentModel]:
    page = list(members)
    if not page:
        return page
    permissions = PermissionService()
    demandeur_role = permissions.authorize(
        action=PermissionAction.LIST_RECRUTEMENT_AGENTS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    for member in page:
        member.authorized_actions = [  # type: ignore[attr-defined]
            action.value
            for action in permissions.authorized_actions_member(
                demandeur_role=demandeur_role,
                demandeur_id=utilisateur.username,
                member=member,
            )
        ]
    return page
