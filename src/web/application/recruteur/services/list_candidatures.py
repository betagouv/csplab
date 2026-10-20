from uuid import UUID

from django.db.models import QuerySet

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.users.models import UserModel


def list_candidatures(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    utilisateur: UserModel,
) -> QuerySet[CandidatureModel]:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    ).check_recrutement_belongs_to_organisme()

    return CandidatureModel.objects.by_recrutement(recrutement_id)
