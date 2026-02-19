"""VectorizedDocument Django model for pgvector storage."""

from django.db import models
from pgvector.django import VectorField

from domain.entities.document import DocumentType
from domain.entities.vectorized_document import VectorizedDocument


class VectorizedDocumentModel(models.Model):
    """Django model for vectorized documents with pgvector support."""

    id = models.UUIDField(primary_key=True)
    entity_id = models.UUIDField(db_index=True)
    document_type = models.CharField(
        max_length=20,
        choices=[(dt.value, dt.value) for dt in DocumentType],
        db_index=True,
    )
    content = models.TextField()
    embedding = VectorField(dimensions=3072)
    metadata = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Model metadata."""

        db_table = "vectorized_documents"
        verbose_name = "VectorizedDocument"
        verbose_name_plural = "VectorizedDocuments"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["id", "document_type"],
                name="unique_id_document_type",
            ),
        ]

    def __str__(self):
        """String representation."""
        return f"VectorizedDocument(id={self.id}, entity_id={self.entity_id})"

    def to_entity(self) -> VectorizedDocument:
        """Convert Django model to domain entity."""
        return VectorizedDocument(
            id=self.id,
            entity_id=self.entity_id,
            document_type=DocumentType(self.document_type),
            content=self.content,
            embedding=list(self.embedding),
            metadata=self.metadata,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_entity(cls, entity: VectorizedDocument) -> "VectorizedDocumentModel":
        """Create Django model from domain entity."""
        return cls(
            id=entity.id,
            entity_id=entity.entity_id,
            document_type=entity.document_type.value,
            content=entity.content,
            embedding=entity.embedding,
            metadata=entity.metadata,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
