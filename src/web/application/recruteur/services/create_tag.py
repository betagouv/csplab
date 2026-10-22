from uuid import UUID, uuid4

from ddd.entity import Entity
from django.db import IntegrityError, transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.tag_errors import TagAlreadyExists
from domain.recruteur.tag_rules import normalize_tag_name
from infrastructure.django_apps.tag.models import TagCategory, TagColor, TagModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)

TAG_NAME_UNIQUE_CONSTRAINT = "tag_unique_name_per_organisme_category"


def create_tag(
    *,
    organisme_id: UUID,
    utilisateur: UserModel,
    name: str,
    category: TagCategory,
    color: TagColor = TagColor.BLEU,
) -> TagModel:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.CREATE_TAG,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )
    name = normalize_tag_name(name)

    with transaction.atomic():
        try:
            tag = TagModel.objects.create(
                id=uuid4(),
                organisme_id=organisme_id,
                name=name,
                category=category,
                color=color,
            )
        except IntegrityError as exc:
            if TAG_NAME_UNIQUE_CONSTRAINT in str(exc):
                raise TagAlreadyExists(name) from exc
            raise
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=tag.id),
            ressource_kind="Tag",
            event_name="TagCree",
        )
    return tag
