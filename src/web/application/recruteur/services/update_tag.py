from uuid import UUID

from ddd.entity import Entity
from django.db import IntegrityError, transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.tag_errors import TagAlreadyExists, TagNotFound
from infrastructure.django_apps.tag.models import TagColor, TagModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def update_tag(
    *,
    organisme_id: UUID,
    tag_id: UUID,
    utilisateur: UserModel,
    name: str,
    color: TagColor,
) -> TagModel:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.UPDATE_TAG,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    with transaction.atomic():
        try:
            # TODO : la course lecture/écriture concurrente n'est pas testée
            # (pas critique pour les étiquettes, revue #2036)
            tag = TagModel.objects.by_id(organisme_id, tag_id).select_for_update().get()
        except TagModel.DoesNotExist as exc:
            raise TagNotFound(tag_id) from exc

        tag.name = name
        tag.color = color
        try:
            tag.save(update_fields=["updated_at", "name", "color"])
        except IntegrityError as exc:
            raise TagAlreadyExists(tag.name) from exc
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=tag.id),
            ressource_kind="Tag",
            event_name="TagModifie",
        )
    return tag
