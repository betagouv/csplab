from uuid import UUID

from ddd.entity import Entity
from django.db.models import QuerySet

from application.identite.context_services.permission_service import (
    PermissionService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.permission_action import PermissionAction
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def list_organisme_agents(
    *, organisme_id: UUID, utilisateur: UserModel
) -> QuerySet[OrganismeAgentModel]:
    PermissionService().authorize(
        action=PermissionAction.LIST_ORGANISME_AGENTS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    agents = (
        OrganismeAgentModel.objects.by_organisme(organisme_id)
        .active()
        .with_agent_profile()
    )
    AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
        utilisateur_id=utilisateur.username,
        entity=Entity(entity_id=organisme_id),
        ressource_kind="OrganismeRecruteur",
        event_name="OrganismeAgentsConsultes",
    )
    return agents
