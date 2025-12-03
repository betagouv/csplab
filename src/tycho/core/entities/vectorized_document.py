"""VectorizedDocument entity for semantic search operations."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class VectorizedDocument:
    """VectorizedDocument entity representing a document with its semantic embedding."""

    id: int
    document_id: int
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
