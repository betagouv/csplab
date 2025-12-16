"""VectorizedDocument entity for semantic search operations."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from core.entities.document import DocumentType
from core.interfaces.entity_interface import IEntity


@dataclass
class VectorizedDocument(IEntity):
    """VectorizedDocument entity representing a document with its semantic embedding."""

    id: int
    document_id: int
    document_type: DocumentType
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
