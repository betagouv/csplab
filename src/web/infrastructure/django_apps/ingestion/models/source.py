from django.db import models

from domain.entities.source import Source
from domain.value_objects.source_type import SourceType


class SourceModel(models.Model):
    objects: models.Manager = models.Manager()

    id = models.UUIDField(primary_key=True)
    source_id = models.UUIDField(unique=True)
    type = models.CharField(
        max_length=50, choices=[(st.value, st.value) for st in SourceType]
    )
    client_id_front = models.CharField(max_length=255)
    client_id_back = models.CharField(max_length=255)
    base_url = models.URLField(max_length=255)

    class Meta:
        db_table = "source"
        verbose_name = "Source"
        verbose_name_plural = "Sources"

    def to_entity(self) -> Source:
        return Source(
            id=self.id,
            source_id=self.source_id,
            type=SourceType(self.type),
            client_id_front=self.client_id_front,
            client_id_back=self.client_id_back,
            base_url=self.base_url,
        )

    @classmethod
    def from_entity(cls, source: Source) -> "SourceModel":
        return cls(
            id=source.id,
            source_id=source.source_id,
            type=source.type.value,
            client_id_front=source.client_id_front,
            client_id_back=source.client_id_back,
            base_url=source.base_url,
        )

    def __str__(self) -> str:
        return f"{self.type} - {self.base_url}"
