from uuid import UUID

from ddd.entity import Entity
from django.db import transaction

from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.errors.tag_errors import TagNotOnCandidature
from infrastructure.django_apps.tag.models import CandidatureTagModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def remove_candidature_tag(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    tag_id: UUID,
    utilisateur: UserModel,
) -> None:
    candidature_service = CandidatureAgentService(
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
        candidature_id=candidature_id,
        utilisateur=utilisateur,
    )
    candidature_service.check_accessible(
        PermissionAction.MANAGE_TAG_ON_APPLICATION, check_candidature=False
    )

    with transaction.atomic():
        candidature_service.lock_candidature()

        deleted, _ = CandidatureTagModel.objects.by_candidature_and_tag(
            candidature_id, tag_id
        ).delete()
        if deleted == 0:
            raise TagNotOnCandidature(tag_id)
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=candidature_id),
            ressource_kind="Candidature",
            event_name="EtiquetteRetiree",
        )
