"""Django model for CVMetadata entity."""

from django.db import models

from domain.entities.cv_metadata import CVMetadata
from domain.value_objects.cv_processing_status import CVStatus


class CVMetadataModel(models.Model):
    """Django model for CVMetadata entity persistence."""

    objects: models.Manager = models.Manager()

    id = models.UUIDField(primary_key=True)
    filename = models.CharField(max_length=255)
    extracted_text = models.JSONField(null=True, blank=True)
    search_query = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=[(status.value, status.value) for status in CVStatus]
    )
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        """Meta configuration for CVMetadataModel."""

        db_table = "cv_metadata"
        verbose_name = "CV Metadata"
        verbose_name_plural = "CV Metadata"

    def to_entity(self) -> CVMetadata:
        """Convert Django model to CVMetadata entity."""
        return CVMetadata(
            id=self.id,
            filename=self.filename,
            status=CVStatus(self.status),
            created_at=self.created_at,
            updated_at=self.updated_at,
            extracted_text=self.extracted_text,
            search_query=self.search_query,
        )

    @classmethod
    def from_entity(cls, cv_metadata: CVMetadata) -> "CVMetadataModel":
        """Create Django model from CVMetadata entity."""
        return cls(
            id=cv_metadata.id,
            filename=cv_metadata.filename,
            extracted_text=cv_metadata.extracted_text,
            search_query=cv_metadata.search_query,
            status=cv_metadata.status.value,
            created_at=cv_metadata.created_at,
            updated_at=cv_metadata.updated_at,
        )

    def __str__(self) -> str:
        """String representation of CVMetadataModel."""
        return f"{self.filename} - {self.id}"
