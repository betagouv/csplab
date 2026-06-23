from typing import Optional
from uuid import UUID, uuid4

from faker import Faker

from domain.ingestion.entities.source import Source
from domain.ingestion.value_objects.source_type import SourceType
from infrastructure.django_apps.ingestion.models.source import SourceModel

fake = Faker()


class SourceFactory:
    @staticmethod
    def create_entity(
        source_id: Optional[UUID] = None,
        slug: str = "talentsoft",
        type: SourceType = SourceType.TALENTSOFT,
        client_id_front: str = "client_front",
        client_id_back: str = "client_back",
        base_url_front: Optional[str] = None,
        base_url_back: Optional[str] = None,
    ) -> Source:
        return Source(
            source_id=source_id or uuid4(),
            slug=slug,
            type=type,
            client_id_front=client_id_front,
            client_id_back=client_id_back,
            base_url_front=base_url_front or fake.url(),
            base_url_back=base_url_back or fake.url(),
        )

    @staticmethod
    def create_model(**kwargs) -> SourceModel:
        entity = SourceFactory.create_entity(**kwargs)
        model = SourceModel.from_entity(entity)
        model.save()
        return model
