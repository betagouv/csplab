from uuid import UUID

from django.db.models import QuerySet

from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
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


def list_recrutement_agents(
    *, organisme_id: UUID, recrutement_id: UUID, utilisateur: Utilisateur
) -> QuerySet[RecrutementAgentModel]:
    # TODO : to refactor in ADR-009 style once OrganismePermissionService is migrated
    organisme_permission_service = OrganismePermissionService(
        organisme_recruteur_repository=PostgresOrganismeRecruteurRepository(),
        organisme_agent_repository=PostgresOrganismeAgentRepository(),
        recrutement_agent_repository=PostgresRecrutementAgentRepository(),
    )
    organisme_permission_service.est_autorise(
        action=OrganismeAction.LIST_RECRUTEMENT_AGENTS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    if not RecrutementModel.objects.filter(
        pk=recrutement_id, organisme_id=organisme_id
    ).exists():
        raise RecrutementInexistant(recrutement_id)

    return RecrutementAgentModel.objects.by_recrutement(recrutement_id)
