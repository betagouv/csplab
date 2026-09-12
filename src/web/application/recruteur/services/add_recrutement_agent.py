from uuid import UUID, uuid4

from ddd.entity import Entity
from django.db import transaction
from django.db import IntegrityError, transaction

from application.identite.context_services.organisme_permission_service import (
    can_execute,
)
from application.recruteur.context_services.recrutement_agent_context_service import (
    RecrutementAgentContextService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
)
from infrastructure.django_apps.users.models import ProfilAgentModel
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
    can_execute(
        action=OrganismeAction.ADD_RECRUTEMENT_AGENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    if not ProfilAgentModel.objects.filter(
        utilisateur_id=agent_id  # type: ignore[misc]
    ).exists():
        raise ProfilAgentNexistePas(agent_id)

    contexte = RecrutementAgentContextService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    contexte.check_recrutement_belongs_to_organisme()
    contexte.check_agent_attached_to_organisme(agent_id)
    contexte.check_agent_not_active_member(agent_id)

    with transaction.atomic():
        recrutement_agent, created = RecrutementAgentModel.objects.update_or_create(
            recrutement_id=recrutement_id,
            agent_id=agent_id,  # type: ignore[misc]
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
