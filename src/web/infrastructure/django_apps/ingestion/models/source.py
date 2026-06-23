from uuid import uuid4

from django.db import models

from domain.ingestion.entities.source import Source
from domain.ingestion.value_objects.source_type import SourceType
from infrastructure.django_apps.utils.models import BaseDatedModel


class SourceModel(BaseDatedModel):
    source_id = models.UUIDField(unique=True, default=uuid4)
    slug = models.SlugField(max_length=255)
    type = models.CharField(
        max_length=50, choices=[(st.value, st.value) for st in SourceType]
    )
    client_id_front = models.CharField(max_length=255)
    client_id_back = models.CharField(max_length=255)
    base_url_front = models.URLField()
    base_url_back = models.URLField()

    class Meta:
        db_table = "sources"
        verbose_name = "Source"
        verbose_name_plural = "Sources"

    def to_entity(self) -> Source:
        return Source(
            entity_id=self.id,
            source_id=self.source_id,
            slug=self.slug,
            type=SourceType(self.type),
            client_id_front=self.client_id_front,
            client_id_back=self.client_id_back,
            base_url_front=self.base_url_front,
            base_url_back=self.base_url_back,
        )

    @classmethod
    def from_entity(cls, source: Source) -> "SourceModel":
        return cls(
            id=source.entity_id,
            source_id=source.source_id,
            slug=source.slug,
            type=source.type.value,
            client_id_front=source.client_id_front,
            client_id_back=source.client_id_back,
            base_url_front=source.base_url_front,
            base_url_back=source.base_url_back,
        )

    def __str__(self) -> str:
        return f"{self.type} - {self.base_url_front}"
