from uuid import UUID

from application.ingestion.errors.application_errors_ingestion import (
    SourceIntrouvable,
)
from infrastructure.django_apps.ingestion.models.source import SourceModel


def get_source(source_id: UUID) -> SourceModel:
    try:
        return SourceModel.objects.get(source_id=source_id)
    except SourceModel.DoesNotExist as e:
        raise SourceIntrouvable(source_id) from e
