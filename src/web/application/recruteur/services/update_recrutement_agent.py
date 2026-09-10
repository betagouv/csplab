from uuid import UUID

from ddd.entity import Entity
from django.db import transaction

from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.organisme_agent_errors import AgentNonRattache
from domain.recruteur.errors.recrutement_agent_errors import AgentNonMembreRecrutement
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
    RecrutementModel,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from infrastructure.repositories.recruteur.postgres_organisme_agent_repository import (
    PostgresOrganismeAgentRepository,
)
from infrastructure.repositories.recruteur.postgres_organisme_repository import (
    PostgresOrganismeRecruteurRepository,
)
from infrastructure.repositories.recruteur.postgres_recrutement_agent_repository import (  # noqa: E501
    PostgresRecrutementAgentRepository,
)


def update_recrutement_agent(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    agent_id: UUID,
    role: str,
    utilisateur: Utilisateur,
) -> RecrutementAgentModel:
    # TODO : to refactor in ADR-009 style once OrganismePermissionService is migrated
    organisme_permission_service = OrganismePermissionService(
        organisme_recruteur_repository=PostgresOrganismeRecruteurRepository(),
        organisme_agent_repository=PostgresOrganismeAgentRepository(),
        recrutement_agent_repository=PostgresRecrutementAgentRepository(),
    )
    organisme_permission_service.est_autorise(
        action=OrganismeAction.UPDATE_RECRUTEMENT_AGENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    if not RecrutementModel.objects.filter(
        pk=recrutement_id, organisme_id=organisme_id
    ).exists():
        raise RecrutementInexistant(recrutement_id)

    agent_rattache_a_organisme = OrganismeAgentModel.objects.filter(
        organisme_id=organisme_id,
        agent_id=agent_id,  # type: ignore[misc]
        date_revocation__isnull=True,
    ).exists()
    if not agent_rattache_a_organisme:
        raise AgentNonRattache(organisme_id, agent_id)

    try:
        recrutement_agent = RecrutementAgentModel.objects.get(
            recrutement_id=recrutement_id,
            agent_id=agent_id,  # type: ignore[misc]
        )
    except RecrutementAgentModel.DoesNotExist as error:
        raise AgentNonMembreRecrutement(recrutement_id, agent_id) from error

    with transaction.atomic():
        recrutement_agent.role = role
        recrutement_agent.save(update_fields=["role", "updated_at"])
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.entity_id,
            entity=Entity(entity_id=agent_id),
            ressource_kind="RecrutementAgent",
            event_name="AgentRecrutementRoleModifie",
        )

    return recrutement_agent
