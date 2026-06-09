from dataclasses import dataclass, field
from typing import Any, Dict, List
from uuid import UUID, uuid4

from ddd.entity import Entity

from domain.ingestion.entities.document import DocumentType


@dataclass(kw_only=True)
class VectorizedDocument(Entity):
    document_type: DocumentType
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
    entity_id: UUID = field(default_factory=uuid4)
