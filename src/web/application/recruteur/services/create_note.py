from uuid import UUID, uuid4

from ddd.entity import Entity
from django.db import transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def create_note(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    message: str,
    utilisateur: Utilisateur,
) -> NoteModel:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.CREATE_NOTE,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    contexte = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    contexte.check_recrutement_belongs_to_organisme()
    contexte.check_candidature_belongs_to_recrutement(candidature_id)

    publie_par_id = utilisateur.entity_id

    with transaction.atomic():
        note = NoteModel.objects.create(
            id=uuid4(),
            candidature_id=candidature_id,
            publie_par_id=publie_par_id,
            message=message,
        )
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=publie_par_id,
            entity=Entity(entity_id=note.id),
            ressource_kind="Note",
            event_name="NoteAjoutee",
        )
    return note
