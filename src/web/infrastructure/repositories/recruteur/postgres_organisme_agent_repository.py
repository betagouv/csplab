from datetime import datetime
from uuid import UUID, uuid4

from django.db import IntegrityError, transaction

from domain.recruteur.errors.organisme_agent_errors import (
    AgentDejaRattache,
    AgentNonRattache,
)
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

    def is_revoked(self, *, organisme_id: UUID, agent_id: UUID) -> bool | None:
        try:
            liaison = OrganismeAgentModel.objects.get(
                organisme_id=organisme_id,
                agent_id=agent_id,  # type: ignore[misc]
            )
        except OrganismeAgentModel.DoesNotExist:
            return None
        return liaison.date_revocation is not None

    def reattach(
        self, *, organisme_id: UUID, agent_id: UUID, role: AgentOrganismeRole
    ) -> None:
        updated = OrganismeAgentModel.objects.filter(
            organisme_id=organisme_id,
            agent_id=agent_id,  # type: ignore[misc]
        ).update(role=role.value, date_revocation=None)
        if updated == 0:
            raise AgentNonRattache(organisme_id, agent_id)

    def update_role(
        self, *, organisme_id: UUID, agent_id: UUID, role: AgentOrganismeRole
    ) -> None:
        updated = OrganismeAgentModel.objects.filter(
            organisme_id=organisme_id,
            agent_id=agent_id,  # type: ignore[misc]
        ).update(role=role.value)
        if updated == 0:
            raise AgentNonRattache(organisme_id, agent_id)

    def revoke(
        self, *, organisme_id: UUID, agent_id: UUID, date_revocation: datetime
    ) -> None:
        updated = OrganismeAgentModel.objects.filter(
            organisme_id=organisme_id,
            agent_id=agent_id,  # type: ignore[misc]
        ).update(date_revocation=date_revocation)
        if updated == 0:
            raise AgentNonRattache(organisme_id, agent_id)
