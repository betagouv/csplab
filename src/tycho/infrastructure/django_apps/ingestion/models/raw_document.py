"""Django models for legal document ingestion."""

from django.db import models

from domain.entities.document import Document, DocumentType


class RawDocument(models.Model):
    """Model for storing raw ingres employement body."""

    id = models.UUIDField(primary_key=True)
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
    processed_at = models.DateTimeField(null=True, blank=True)
    error_msg = models.TextField(null=True, blank=True)

    class Meta:
        """Meta configuration for RawDocument model."""

        verbose_name = "RawDocument"
        verbose_name_plural = "RawDocument"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["external_id", "document_type"],
                name="unique_external_id_document_type",
            ),
        ]

    def to_entity(self) -> Document:
        """Convert to core entity."""
        return Document(
            id=self.id,
            external_id=self.external_id,
            raw_data=self.raw_data,
            type=DocumentType(self.document_type),  # String -> Enum
            created_at=self.created_at,
            updated_at=self.updated_at,
            processed_at=self.processed_at,
            error_msg=self.error_msg,
        )

    @classmethod
    def from_entity(cls, document: Document) -> "RawDocument":
        """Create Django model **instance** from Document entity."""
        return cls(
            id=document.id,
            external_id=document.external_id,
            raw_data=document.raw_data,
            document_type=document.type.value if document.type else None,
            created_at=document.created_at,
            updated_at=document.updated_at,
            processed_at=document.processed_at,
            error_msg=document.error_msg,
        )
