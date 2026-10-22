from collections.abc import Iterable
from uuid import UUID

from django.db.models import QuerySet

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.errors.organisme_permission_errors import OperationOrganismeRefusee
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
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
    permissions = OrganismePermissionService()
    page = list(recrutements)
    for recrutement in page:
        recrutement_role = recrutement.recrutement_role  # type: ignore[attr-defined]
        recrutement.authorized_actions = [  # type: ignore[attr-defined]
            action.value
            for action in permissions.authorized_actions_recrutement(
                AgentOrganismeRole(recrutement.organisme_role),  # type: ignore[attr-defined]
                recrutement_role=(
                    AgentRecrutementRole(recrutement_role) if recrutement_role else None
                ),
            )
        ]
    return page


def list_actives_recrutements(
    *, organisme_id: UUID, utilisateur: UserModel
) -> QuerySet[RecrutementModel]:
    return (
        _agent_recrutements(organisme_id=organisme_id, utilisateur=utilisateur)
        .actives()
        .with_responsables()
        .with_compteurs_candidatures()
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
        .order_by("offre_id")
    )
