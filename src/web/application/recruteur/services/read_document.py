from typing import NamedTuple
from uuid import UUID

import filetype
from django.conf import settings

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.recrutement_errors import (
    RecrutementDocumentTypeNonAutorise,
)
from infrastructure.django_apps.candidate.models.document import DocumentModel


class DocumentDownload(NamedTuple):
    document: DocumentModel
    content_type: str


def read_document(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    document_id: UUID,
    utilisateur: Utilisateur,
) -> DocumentDownload:
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

    document = DocumentModel.objects.get(id=document_id)
    with document.fichier.open("rb") as fichier:
        detected = filetype.guess(fichier.read(262))
    content_type = detected.mime if detected else "inconnu"
    if content_type not in settings.ALLOWED_DOCUMENT_CONTENT_TYPES:
        raise RecrutementDocumentTypeNonAutorise(document_id, content_type)

    return DocumentDownload(document=document, content_type=content_type)
