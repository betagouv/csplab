from uuid import UUID

from ddd.entity import Entity
from django.db import transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.errors.organisme_agent_errors import AgentNonRattache
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def update_organisme_agent(
    *,
    organisme_id: UUID,
    agent_id: UUID,
    role: AgentOrganismeRole,
    utilisateur: UserModel,
) -> OrganismeAgentModel:
    OrganismePermissionService().can_execute(
        action=PermissionAction.UPDATE_ORGANISME_AGENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    liaisons = OrganismeAgentModel.objects.any_status_by_organisme_and_agent(
        organisme_id, agent_id
    )
    with transaction.atomic():
        if not liaisons.update(role=role.value):
            raise AgentNonRattache(organisme_id, agent_id)
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=agent_id),
            ressource_kind="AgentOrganisme",
            event_name="AgentOrganismeRoleModifie",
        )
        return liaisons.with_agent_profile().get()
