from uuid import UUID, uuid4

from ddd.entity import Entity
from django.db import IntegrityError, transaction

from application.identite.context_services.permission_service import (
    PermissionService,
)
from application.recruteur.context_services.organisme_agent_service import (
    get_profil_agent,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.errors.organisme_agent_errors import AgentDejaRattache
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def attach_organisme_agent(
    *,
    organisme_id: UUID,
    agent_id: UUID,
    role: AgentOrganismeRole,
    utilisateur: UserModel,
) -> OrganismeAgentModel:
    PermissionService().can_execute(
        action=PermissionAction.ATTACH_ORGANISME_AGENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )
    get_profil_agent(agent_id)

    liaisons = OrganismeAgentModel.objects.any_status_by_organisme_and_agent(
        organisme_id, agent_id
    )
    with transaction.atomic():
        if not liaisons.revoked().update(role=role.value, date_revocation=None):
            try:
                OrganismeAgentModel.objects.create(
                    id=uuid4(),
                    organisme_id=organisme_id,
                    agent_id=agent_id,
                    role=role.value,
                )
            except IntegrityError as error:
                raise AgentDejaRattache(organisme_id, agent_id) from error
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=agent_id),
            ressource_kind="AgentOrganisme",
            event_name="AgentOrganismeRoleAttache",
        )
        return liaisons.with_agent_profile().get()
