"""Document entity for raw data storage."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from domain.interfaces.entity_interface import IEntity


class DocumentType(Enum):
    """Enumeration of document types for raw data ingestion."""

    CORPS = "CORPS"
    GRADE = "GRADE"
    CONCOURS = "CONCOURS"
    CONCOURS_LAW = "CONCOURS_LAW"
    CONCOURS_LAW_DETAILS = "CONCOURS_LAW_DETAILS"
    OFFERS = "OFFERS"

    def __str__(self):
        """Return string representation."""
        return self.value


@dataclass
class Document(IEntity):
    """Document entity representing any type of raw ingested data."""

    external_id: Optional[str]
    raw_data: Dict[str, Any]
    type: DocumentType
    created_at: datetime
    updated_at: datetime
    error_msg: Optional[str] = None
    id: UUID = field(default_factory=uuid4)
