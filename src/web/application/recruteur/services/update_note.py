from uuid import UUID

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
from domain.recruteur.errors.note_errors import NoteIntrouvable
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def update_note(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    note_id: UUID,
    message: str,
    utilisateur: Utilisateur,
) -> NoteModel:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.UPDATE_NOTE,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    contexte = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    contexte.check_recrutement_belongs_to_organisme()
    contexte.check_candidature_belongs_to_recrutement(candidature_id)

    try:
        note = NoteModel.objects.by_candidature_author_and_id(
            candidature_id, utilisateur.entity_id, note_id
        ).get()
    except NoteModel.DoesNotExist as error:
        raise NoteIntrouvable(note_id) from error

    with transaction.atomic():
        note.message = message
        note.save(update_fields=["message", "updated_at"])
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.entity_id,
            entity=Entity(entity_id=note.id),
            ressource_kind="Note",
            event_name="NoteEditee",
        )
    return note
