from uuid import UUID

from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.organisme_agent_errors import AgentNonRattache
from domain.recruteur.errors.recrutement_agent_errors import (
    AgentDejaMembreRecrutement,
    AgentNonMembreRecrutement,
)
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
    RecrutementModel,
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


def can_execute(
    *, action: OrganismeAction, utilisateur: Utilisateur, organisme_id: UUID
) -> None:
    # TODO : to refactor in ADR-009 style once OrganismePermissionService is migrated
    organisme_permission_service = OrganismePermissionService(
        organisme_recruteur_repository=PostgresOrganismeRecruteurRepository(),
        organisme_agent_repository=PostgresOrganismeAgentRepository(),
        recrutement_agent_repository=PostgresRecrutementAgentRepository(),
    )
    organisme_permission_service.est_autorise(
        action=action, utilisateur=utilisateur, organisme_id=organisme_id
    )


class RecrutementAgentContextService:
    def __init__(self, *, organisme_id: UUID, recrutement_id: UUID) -> None:
        self.organisme_id = organisme_id
        self.recrutement_id = recrutement_id

    def check_recrutement_belongs_to_organisme(self) -> None:
        if not RecrutementModel.objects.filter(
            pk=self.recrutement_id, organisme_id=self.organisme_id
        ).exists():
            raise RecrutementInexistant(self.recrutement_id)

    def check_agent_attached_to_organisme(self, agent_id: UUID) -> None:
        if (
            not OrganismeAgentModel.objects.active()
            .filter(
                organisme_id=self.organisme_id,
                agent_id=agent_id,  # type: ignore[misc]
            )
            .exists()
        ):
            raise AgentNonRattache(self.organisme_id, agent_id)

    def check_agent_not_active_member(self, agent_id: UUID) -> None:
        if (
            RecrutementAgentModel.objects.active()
            .filter(
                recrutement_id=self.recrutement_id,
                agent_id=agent_id,  # type: ignore[misc]
            )
            .exists()
        ):
            raise AgentDejaMembreRecrutement(self.recrutement_id, agent_id)

    def get_active_member(self, agent_id: UUID) -> RecrutementAgentModel:
        try:
            return RecrutementAgentModel.objects.active().get(
                recrutement_id=self.recrutement_id,
                agent_id=agent_id,  # type: ignore[misc]
            )
        except RecrutementAgentModel.DoesNotExist as error:
            raise AgentNonMembreRecrutement(self.recrutement_id, agent_id) from error
