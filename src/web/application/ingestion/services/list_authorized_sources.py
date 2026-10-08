from application.ingestion.context_services.can_view_sources import can_view_sources
from application.ingestion.errors.application_errors_ingestion import (
    AccesSourcesRefuse,
)
from infrastructure.django_apps.ingestion.models.source import (
    SourceModel,
    SourceQuerySet,
)
from infrastructure.django_apps.users.models import UserModel


def list_authorized_sources(user: UserModel) -> SourceQuerySet:
    if not can_view_sources(user):
        raise AccesSourcesRefuse(user.username)
    return SourceModel.objects.authorized_for(user).order_by("slug")
