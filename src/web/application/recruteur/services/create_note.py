from uuid import UUID, uuid4

from ddd.entity import Entity
from django.db import transaction

from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.permission_action import PermissionAction
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.django_apps.tag.models import NoteTagModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def create_note(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    message: str,
    utilisateur: UserModel,
    est_privee: bool = False,
) -> NoteModel:
    candidature_service = CandidatureAgentService(
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
        candidature_id=candidature_id,
        utilisateur=utilisateur,
    )
    candidature_service.check_accessible(PermissionAction.CREATE_NOTE)

    publie_par_id = utilisateur.username

    with transaction.atomic():
        note = NoteModel.objects.create(
            id=uuid4(),
            candidature_id=candidature_id,
            publie_par_id=publie_par_id,
            message=message,
            est_privee=est_privee,
        )
        # note neuve : cache de prefetch vide, aucune étiquette à relire
        note._prefetched_objects_cache = {  # type: ignore[attr-defined]
            "tags_liaisons": NoteTagModel.objects.none()
        }
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=publie_par_id,
            entity=Entity(entity_id=note.id),
            ressource_kind="Note",
            event_name="NoteAjoutee",
        )
    return note
