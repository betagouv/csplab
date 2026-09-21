from uuid import UUID, uuid4

from ddd.entity import Entity
from django.db import transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.organisme_agent_service import (
    attach_agent_to_organisme,
    get_profil_agent,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
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


def add_recrutement_agent(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    agent_id: UUID,
    role: str,
    utilisateur: Utilisateur,
) -> RecrutementAgentModel:
    # TODO : to refactor in ADR-009 style
    OrganismePermissionService().can_execute(
        action=OrganismeAction.ADD_RECRUTEMENT_AGENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    agent = get_profil_agent(agent_id)

    contexte = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    contexte.check_recrutement_belongs_to_organisme()
    contexte.check_agent_not_active_member(agent_id)

    with transaction.atomic():
        attach_agent_to_organisme(
            organisme_id=organisme_id, agent=agent, utilisateur=utilisateur
        )
        recrutement_agent, created = RecrutementAgentModel.objects.update_or_create(
            recrutement_id=recrutement_id,
            agent=agent,
            defaults={"role": role, "date_revocation": None},
            create_defaults={"id": uuid4(), "role": role},
        )
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.entity_id,
            entity=Entity(entity_id=agent_id),
            ressource_kind="RecrutementAgent",
            event_name=(
                "AgentRecrutementAjoute" if created else "AgentRecrutementReintegre"
            ),
        )

    return recrutement_agent
