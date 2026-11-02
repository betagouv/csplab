from django.db.models import QuerySet

from infrastructure.django_apps.ingestion.models.source import SourceModel


def list_sources() -> QuerySet[SourceModel]:
    return SourceModel.objects.order_by("slug")
