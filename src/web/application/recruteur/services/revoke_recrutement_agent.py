from uuid import UUID

from ddd.entity import Entity
from django.db import transaction
from django.utils import timezone

from application.identite.context_services.organisme_permission_service import (
    can_execute,
)
from application.recruteur.context_services.recrutement_agent_context_service import (
    RecrutementAgentContextService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def revoke_recrutement_agent(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    agent_id: UUID,
    utilisateur: Utilisateur,
) -> RecrutementAgentModel:
    can_execute(
        action=OrganismeAction.REVOKE_RECRUTEMENT_AGENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    contexte = RecrutementAgentContextService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    contexte.check_recrutement_belongs_to_organisme()
    contexte.check_agent_attached_to_organisme(agent_id)
    recrutement_agent = contexte.get_active_member(agent_id)

    with transaction.atomic():
        recrutement_agent.date_revocation = timezone.now()
        recrutement_agent.save(update_fields=["date_revocation", "updated_at"])
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.entity_id,
            entity=Entity(entity_id=agent_id),
            ressource_kind="RecrutementAgent",
            event_name="AgentRecrutementRevoque",
        )

    return recrutement_agent
