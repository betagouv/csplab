from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.tag_errors import TagNotOnCandidature
from infrastructure.django_apps.tag.models import CandidatureTagModel
from infrastructure.django_apps.users.models import UserModel


def remove_candidature_tag(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    tag_id: UUID,
    utilisateur: UserModel,
) -> None:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.ADD_TAG_TO_APPLICATION,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    contexte = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    contexte.check_recrutement_belongs_to_organisme()
    candidature_service = CandidatureAgentService(
        recrutement_id=recrutement_id, candidature_id=candidature_id
    )
    candidature_service.check_candidature_belongs_to_recrutement()

    deleted, _ = CandidatureTagModel.objects.by_candidature_and_tag(
        candidature_id, tag_id
    ).delete()
    if deleted == 0:
        raise TagNotOnCandidature(tag_id)
