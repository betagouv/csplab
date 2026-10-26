from uuid import UUID

from ddd.entity import Entity
from django.db import transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.tag_errors import TagNotFound
from infrastructure.django_apps.tag.models import TagModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def delete_tag(*, organisme_id: UUID, tag_id: UUID, utilisateur: UserModel) -> None:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.DELETE_TAG,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    with transaction.atomic():
        deleted, _ = TagModel.objects.by_id(organisme_id, tag_id).delete()
        if deleted == 0:
            raise TagNotFound(tag_id)
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=tag_id),
            ressource_kind="Tag",
            event_name="TagSupprime",
        )
