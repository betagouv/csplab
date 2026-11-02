from uuid import UUID

from django.db.models import QuerySet

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.tag.models import TagCategory, TagModel
from infrastructure.django_apps.users.models import UserModel


def list_tags(
    *,
    organisme_id: UUID,
    utilisateur: UserModel,
    category: TagCategory | None = None,
) -> QuerySet[TagModel]:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.LIST_TAGS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )
    tags = (
        TagModel.objects.by_category(organisme_id, category)
        if category
        else TagModel.objects.alphabetical(organisme_id)
    )
    return tags.with_usage_count()
