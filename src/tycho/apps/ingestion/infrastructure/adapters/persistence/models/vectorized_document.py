"""VectorizedDocument Django model for pgvector storage."""

from typing import TYPE_CHECKING

from django.db import models
from pgvector.django import VectorField

from core.entities.vectorized_document import VectorizedDocument

if TYPE_CHECKING:
    from django.db.models.manager import Manager


class VectorizedDocumentModel(models.Model):
    """Django model for vectorized documents with pgvector support."""

    document_id = models.IntegerField(unique=True, db_index=True)
    content = models.TextField()
    embedding = VectorField(dimensions=3072)
    metadata = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    if TYPE_CHECKING:
        id: int
        objects: "Manager[VectorizedDocumentModel]"

    class Meta:
        """Model metadata."""

        db_table = "vectorized_documents"

    def __str__(self):
        """String representation."""
        return f"VectorizedDocument(id={self.id}, document_id={self.document_id})"

    def to_entity(self) -> VectorizedDocument:
        """Convert Django model to domain entity."""
        return VectorizedDocument(
            id=self.id,
            document_id=self.document_id,
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
            id=entity.id if entity.id else None,
            document_id=entity.document_id,
            content=entity.content,
            embedding=entity.embedding,
            metadata=entity.metadata,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
