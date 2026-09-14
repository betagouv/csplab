from uuid import UUID

from django.db.models import QuerySet

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
)


def list_recrutement_agents(
    *, organisme_id: UUID, recrutement_id: UUID, utilisateur: Utilisateur
) -> QuerySet[RecrutementAgentModel]:
    # TODO : to refactor in ADR-009 style
    OrganismePermissionService().can_execute(
        action=OrganismeAction.LIST_RECRUTEMENT_AGENTS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    contexte = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    contexte.check_recrutement_belongs_to_organisme()

    return RecrutementAgentModel.objects.by_recrutement(recrutement_id)
