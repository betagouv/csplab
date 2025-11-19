"""Django models for legal document ingestion."""

from django.db import models

from core.entities.document import Document, DocumentType


class RawDocument(models.Model):
    """Model for storing raw ingres employement body."""

    id = models.AutoField(primary_key=True)
    raw_data = models.JSONField("RawDocument")
    document_type = models.CharField(
        "Type de document",
        max_length=10,
        choices=[(dt.value, dt.value) for dt in DocumentType],
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta configuration for RawDocument model."""

        verbose_name = "RawDocument"
        verbose_name_plural = "RawDocument"
        ordering = ["-created_at"]

    def to_entity(self) -> Document:
        """Convert to core entity."""
        return Document(
            id=self.id,
            raw_data=self.raw_data,
            type=DocumentType(self.document_type),  # String -> Enum
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
