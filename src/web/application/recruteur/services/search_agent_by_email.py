from uuid import UUID

from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.users.models import ProfilAgentModel
from infrastructure.repositories.recruteur.postgres_organisme_agent_repository import (
    PostgresOrganismeAgentRepository,
)
from infrastructure.repositories.recruteur.postgres_organisme_repository import (
    PostgresOrganismeRecruteurRepository,
)
from infrastructure.repositories.recruteur.postgres_recrutement_agent_repository import (  # noqa: E501
    PostgresRecrutementAgentRepository,
)


def search_agent_by_email(
    *, organisme_id: UUID, utilisateur: Utilisateur, email: str
) -> ProfilAgentModel | None:
    # TODO : to refactor in ADR-009 style
    organisme_permission_service = OrganismePermissionService(
        organisme_recruteur_repository=PostgresOrganismeRecruteurRepository(),
        organisme_agent_repository=PostgresOrganismeAgentRepository(),
        recrutement_agent_repository=PostgresRecrutementAgentRepository(),
    )
    organisme_permission_service.est_autorise(
        action=OrganismeAction.SEARCH_AGENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    return ProfilAgentModel.objects.par_email(email).first()
