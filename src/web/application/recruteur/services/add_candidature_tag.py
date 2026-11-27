from uuid import UUID

from ddd.entity import Entity
from django.db import transaction

from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.errors.tag_errors import TagNotFound
from infrastructure.django_apps.tag.models import CandidatureTagModel, TagModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def add_candidature_tag(
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
    candidature_service.check_accessible(PermissionAction.MANAGE_TAG_ON_APPLICATION)

    with transaction.atomic():
        try:
            tag = TagModel.objects.by_id(organisme_id, tag_id).select_for_update().get()
        except TagModel.DoesNotExist as error:
            raise TagNotFound(tag_id) from error

        CandidatureTagModel.objects.poser(candidature_id=candidature_id, tag=tag)
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=candidature_id),
            ressource_kind="Candidature",
            event_name="EtiquettePosee",
        )
