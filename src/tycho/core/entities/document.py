"""Document entity for raw data storage."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from core.interfaces.entity_interface import IEntity


class DocumentType(Enum):
    """Enumeration of document types for raw data ingestion."""

    CORPS = "CORPS"
    GRADE = "GRADE"
    CONCOURS = "CONCOURS"
    CONCOURS_LAW = "CONCOURS_LAW"
    CONCOURS_LAW_DETAILS = "CONCOURS_LAW_DETAILS"
    OFFER = "OFFER"

    def __str__(self):
        """Return string representation."""
        return self.value


@dataclass
class Document(IEntity):
    """Document entity representing any type of raw ingested data."""

    id: int
    external_id: Optional[str]
    raw_data: Dict[str, Any]
    type: DocumentType
    created_at: datetime
    updated_at: datetime
