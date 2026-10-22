from uuid import UUID

from ddd.entity import Entity
from django.db import IntegrityError, transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.tag_errors import TagAlreadyExists, TagNotFound
from domain.recruteur.tag_rules import normalize_tag_name
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
    name: str | None = None,
    color: TagColor | None = None,
) -> TagModel:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.UPDATE_TAG,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )
    if name is not None:
        name = normalize_tag_name(name)

    with transaction.atomic():
        try:
            tag = TagModel.objects.by_id(organisme_id, tag_id).get()
        except TagModel.DoesNotExist as exc:
            raise TagNotFound(tag_id) from exc

        update_fields = ["updated_at"]
        if name is not None:
            tag.name = name
            update_fields.append("name")
        if color is not None:
            tag.color = color
            update_fields.append("color")
        try:
            tag.save(update_fields=update_fields)
        except IntegrityError as exc:
            raise TagAlreadyExists(tag.name) from exc
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=tag.id),
            ressource_kind="Tag",
            event_name="TagModifie",
        )
    return tag
