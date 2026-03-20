from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from domain.interfaces.entity_interface import IEntity


class DocumentType(Enum):
    CORPS = "CORPS"
    GRADE = "GRADE"
    CONCOURS = "CONCOURS"
    CONCOURS_LAW = "CONCOURS_LAW"
    CONCOURS_LAW_DETAILS = "CONCOURS_LAW_DETAILS"
    OFFERS = "OFFERS"

    def __str__(self):
        return self.value


@dataclass
class Document(IEntity):
    external_id: Optional[str]
    raw_data: Dict[str, Any]
    type: DocumentType
    created_at: datetime
    processed_at: Optional[datetime] = None
    error_msg: Optional[str] = None
    id: UUID = field(default_factory=uuid4)
