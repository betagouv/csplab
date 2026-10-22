from uuid import UUID

from django.db.models import QuerySet

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
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
    recrutements = RecrutementModel.objects.by_organisme(organisme_id).with_offre()
    if role == AgentOrganismeRole.SUPERVISEUR:
        return recrutements
    return recrutements.by_agent(utilisateur.username)


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
