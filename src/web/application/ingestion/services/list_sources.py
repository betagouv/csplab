from infrastructure.django_apps.ingestion.models.source import (
    SourceModel,
    SourceQuerySet,
)


def list_sources() -> SourceQuerySet:
    return SourceModel.objects.order_by("slug")
