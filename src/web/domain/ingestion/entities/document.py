from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from ddd.entity import Entity


class DocumentType(Enum):
    CORPS = "CORPS"
    GRADE = "GRADE"
    CONCOURS = "CONCOURS"
    OFFERS = "OFFERS"
    METIERS = "METIERS"

    def __str__(self):
        return self.value


@dataclass(kw_only=True)
class Document(Entity):
    raw_data: Dict[str, Any]
    type: DocumentType
    created_at: datetime
    external_id: Optional[str] = None
    processed_at: Optional[datetime] = None
    processing: bool = False
    error_msg: Optional[str] = None
    entity_id: UUID = field(default_factory=uuid4)
