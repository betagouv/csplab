from uuid import UUID

from ddd.entity import Entity
from django.db import transaction

from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.errors.note_errors import NoteIntrouvable
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def editer_note(*, note_id: UUID, message: str, utilisateur_id: UUID) -> NoteModel:
    # TODO : refactor with upcoming RBAC
    try:
        note = NoteModel.objects.active().by_author(utilisateur_id).get(pk=note_id)
    except NoteModel.DoesNotExist as error:
        raise NoteIntrouvable(note_id) from error

    with transaction.atomic():
        note.message = message
        note.save(update_fields=["message", "updated_at"])
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur_id,
            entity=Entity(entity_id=note.id),
            ressource_kind="Note",
            event_name="NoteEditee",
        )
    return note
