from uuid import UUID

from django.db.models import QuerySet

from application.identite.context_services.permission_service import (
    PermissionService,
)
from domain.identite.value_objects.permission_action import PermissionAction
from infrastructure.django_apps.tag.models import TagCategory, TagModel
from infrastructure.django_apps.users.models import UserModel


def list_tags(
    *,
    organisme_id: UUID,
    utilisateur: UserModel,
    category: TagCategory | None = None,
) -> QuerySet[TagModel]:
    PermissionService().can_execute(
        action=PermissionAction.LIST_TAGS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )
    tags = (
        TagModel.objects.by_category(organisme_id, category)
        if category
        else TagModel.objects.alphabetical(organisme_id)
    )
    return tags.with_usage_count()
