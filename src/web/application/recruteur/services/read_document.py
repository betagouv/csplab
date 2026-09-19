from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.candidate.models.document import DocumentModel


def read_document(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    document_id: UUID,
    utilisateur: Utilisateur,
) -> DocumentModel:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.READ_DOCUMENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    service = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    service.check_recrutement_belongs_to_organisme()
    service.check_document_belongs_to_recrutement(candidature_id, document_id)

    return DocumentModel.objects.get(id=document_id)
