from uuid import UUID, uuid4

from ddd.entity import Entity
from django.db import transaction

from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.recruteur.errors.recrutement_errors import CandidatureInexistante
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.django_apps.users.models import ProfilAgentModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def create_note(
    *, candidature_id: UUID, publie_par_id: UUID, message: str
) -> NoteModel:
    if not CandidatureModel.objects.filter(pk=candidature_id).exists():
        raise CandidatureInexistante(candidature_id)
    if not ProfilAgentModel.objects.filter(
        utilisateur__username=publie_par_id
    ).exists():
        raise ProfilAgentNexistePas(publie_par_id)

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
