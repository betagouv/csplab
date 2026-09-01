from uuid import UUID, uuid4

from django.db import IntegrityError, transaction

from domain.recruteur.errors.organisme_agent_errors import AgentDejaRattache
from domain.recruteur.repositories.organisme_agent_repository_interface import (
    IOrganismeAgentRepository,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel


class PostgresOrganismeAgentRepository(IOrganismeAgentRepository):
    def get_role(
        self, *, organisme_id: UUID, agent_id: UUID
    ) -> AgentOrganismeRole | None:
        try:
            liaison = OrganismeAgentModel.objects.get(
                organisme_id=organisme_id,
                agent_id=agent_id,  # type: ignore[misc]
            )
        except OrganismeAgentModel.DoesNotExist:
            return None
        return AgentOrganismeRole(liaison.role)

    def attach(
        self, *, organisme_id: UUID, agent_id: UUID, role: AgentOrganismeRole
    ) -> None:
        try:
            with transaction.atomic():
                OrganismeAgentModel.objects.create(
                    id=uuid4(),
                    organisme_id=organisme_id,
                    agent_id=agent_id,  # type: ignore[misc]
                    role=role.value,
                )
        except IntegrityError as exc:
            raise AgentDejaRattache(organisme_id, agent_id) from exc
