"""Django models for legal document ingestion."""

from django.db import models

from core.entities.document import Document, DocumentType


class RawDocument(models.Model):
    """Model for storing raw ingres employement body."""

    id = models.AutoField(primary_key=True)
    external_id = models.CharField(
        "Identifiant externe",
        max_length=255,
        db_index=True,
        null=True,
        blank=True,
        help_text="NOR pour CONCOURS, corps_id pour CORPS",
    )
    document_type = models.CharField(
        "Type de document",
        max_length=25,
        choices=[(dt.value, dt.value) for dt in DocumentType],
        null=True,
        blank=True,
    )
    raw_data = models.JSONField("RawDocument")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta configuration for RawDocument model."""

        verbose_name = "RawDocument"
        verbose_name_plural = "RawDocument"
        ordering = ["-created_at"]
        unique_together = [("external_id", "document_type")]

    def to_entity(self) -> Document:
        """Convert to core entity."""
        return Document(
            id=self.id,
            external_id=self.external_id,
            raw_data=self.raw_data,
            type=DocumentType(self.document_type),  # String -> Enum
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
