from uuid import UUID, uuid4

from ddd.entity import Entity

from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.users.models import ProfilAgentModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def get_profil_agent(agent_id: UUID) -> ProfilAgentModel:
    try:
        return ProfilAgentModel.objects.get(utilisateur__username=agent_id)
    except ProfilAgentModel.DoesNotExist as error:
        raise ProfilAgentNexistePas(agent_id) from error


def attach_agent_to_organisme(
    *, organisme_id: UUID, agent: ProfilAgentModel, utilisateur: Utilisateur
) -> None:
    """
    Must be called inside a transaction
    """
    if OrganismeAgentModel.objects.by_organisme_and_agent(
        organisme_id, agent.utilisateur_id
    ).exists():
        return

    OrganismeAgentModel.objects.update_or_create(
        organisme_id=organisme_id,
        agent=agent,
        defaults={
            "role": AgentOrganismeRole.AGENT.value,
            "date_revocation": None,
        },
        create_defaults={
            "id": uuid4(),
            "role": AgentOrganismeRole.AGENT.value,
        },
    )
    AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
        utilisateur_id=utilisateur.entity_id,
        entity=Entity(entity_id=agent.utilisateur_id),
        ressource_kind="AgentOrganisme",
        event_name="AgentOrganismeRoleAttache",
    )
