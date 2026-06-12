from dataclasses import dataclass
from typing import Any, Dict, List

from ddd.entity import Entity

from domain.ingestion.entities.document import DocumentType


@dataclass(kw_only=True)
class VectorizedDocument(Entity):
    document_type: DocumentType
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
