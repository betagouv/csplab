from uuid import UUID

from ddd.entity import Entity
from django.db import transaction

from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.errors.note_errors import NoteIntrouvable
from domain.recruteur.errors.tag_errors import TagNotFound
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.django_apps.tag.models import NoteTagModel, TagModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def add_note_tag(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    note_id: UUID,
    tag_id: UUID,
    utilisateur: UserModel,
) -> None:
    candidature_service = CandidatureAgentService(
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
        candidature_id=candidature_id,
        utilisateur=utilisateur,
    )
    candidature_service.check_accessible(PermissionAction.UPDATE_NOTE)

    with transaction.atomic():
        try:
            note = (
                NoteModel.objects.by_candidature_author_and_id(
                    candidature_id, utilisateur.username, note_id
                )
                .select_for_update(of=("self",))
                .get()
            )
        except NoteModel.DoesNotExist as error:
            raise NoteIntrouvable(note_id) from error

        try:
            tag = TagModel.objects.by_id(organisme_id, tag_id).select_for_update().get()
        except TagModel.DoesNotExist as error:
            raise TagNotFound(tag_id) from error

        NoteTagModel.objects.poser(note=note, tag=tag)
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=note_id),
            ressource_kind="Note",
            event_name="EtiquettePosee",
        )
