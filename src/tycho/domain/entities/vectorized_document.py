from dataclasses import dataclass, field
from typing import Any, Dict, List
from uuid import UUID, uuid4

from domain.entities.document import DocumentType
from domain.interfaces.entity_interface import IEntity


@dataclass
class VectorizedDocument(IEntity):
    entity_id: UUID
    document_type: DocumentType
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
    id: UUID = field(default_factory=uuid4)
