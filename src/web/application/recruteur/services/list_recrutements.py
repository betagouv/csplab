from collections.abc import Iterable
from uuid import UUID

from django.db.models import QuerySet

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.authorized_actions import (
    set_authorized_actions,
)
from domain.identite.errors.organisme_permission_errors import OperationOrganismeRefusee
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementModel,
    RecrutementQuerySet,
)
from infrastructure.django_apps.users.models import UserModel


def _agent_recrutements(
    *, organisme_id: UUID, utilisateur: UserModel
) -> RecrutementQuerySet:
    role = OrganismePermissionService().can_execute(
        action=OrganismeAction.LIST_RECRUTEMENTS,
        organisme_id=organisme_id,
        utilisateur=utilisateur,
    )
    if role is None:
        raise OperationOrganismeRefusee()
    recrutements = (
        RecrutementModel.objects.by_organisme(organisme_id)
        .with_offre()
        .with_role_of(utilisateur.username)
        .with_organisme_role(role)
    )
    if role == AgentOrganismeRole.SUPERVISEUR:
        return recrutements
    return recrutements.by_agent(utilisateur.username)


def with_authorized_actions(
    recrutements: Iterable[RecrutementModel],
) -> list[RecrutementModel]:
    page = list(recrutements)
    for recrutement in page:
        set_authorized_actions(recrutement)
    return page


def list_actives_recrutements(
    *, organisme_id: UUID, utilisateur: UserModel
) -> QuerySet[RecrutementModel]:
    return (
        _agent_recrutements(organisme_id=organisme_id, utilisateur=utilisateur)
        .actives()
        .with_responsables()
        .with_compteurs_candidatures()
        .with_unread_conversations(utilisateur.username)
        .order_by("offre_id")
    )


def list_archived_recrutements(
    *, organisme_id: UUID, utilisateur: UserModel
) -> QuerySet[RecrutementModel]:
    return (
        _agent_recrutements(organisme_id=organisme_id, utilisateur=utilisateur)
        .archived()
        .with_responsables()
        .with_recrute()
        .with_unread_conversations(utilisateur.username)
        .order_by("offre_id")
    )
