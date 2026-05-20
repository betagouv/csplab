from uuid import uuid4

from domain.entities.source import Source
from domain.value_objects.source_type import SourceType
from infrastructure.django_apps.ingestion.models.source import SourceModel


class SourceFactory:
    @staticmethod
    def create_entity(
        source_type: SourceType = SourceType.TALENTSOFT,
        client_id_front: str = "client_front",
        client_id_back: str = "client_back",
        base_url: str = "https://example.talentsoft.com",
    ) -> Source:
        return Source(
            id=uuid4(),
            source_id=uuid4(),
            type=source_type,
            client_id_front=client_id_front,
            client_id_back=client_id_back,
            base_url=base_url,
        )

    @staticmethod
    def create_model(**kwargs) -> SourceModel:
        entity = SourceFactory.create_entity(**kwargs)
        model = SourceModel.from_entity(entity)
        model.save()
        return model
