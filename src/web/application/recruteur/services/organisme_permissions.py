from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
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


def organisme_permission_service() -> OrganismePermissionService:
    return OrganismePermissionService(
        organisme_recruteur_repository=PostgresOrganismeRecruteurRepository(),
        organisme_agent_repository=PostgresOrganismeAgentRepository(),
        recrutement_agent_repository=PostgresRecrutementAgentRepository(),
    )
