from typing import List

from domain.ingestion.entities.source import Source
from domain.ingestion.repositories.source_repository_interface import ISourceRepository
from infrastructure.django_apps.ingestion.models.source import SourceModel


class PostgresSourceRepository(ISourceRepository):
    def get_all(self) -> List[Source]:
        return [model.to_entity() for model in SourceModel.objects.all()]
