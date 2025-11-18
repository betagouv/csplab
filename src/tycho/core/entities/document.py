"""Document entity for raw data storage."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict


class DocumentType(Enum):
    """Enumeration of document types for raw data ingestion."""

    CORPS = "CORPS"
    GRADE = "GRADE"
    EXAMINATION = "EXAMINATION"

    def __str__(self):
        """Return string representation."""
        return self.value


@dataclass
class Document:
    """Document entity representing any type of raw ingested data."""

    id: int
    raw_data: Dict[str, Any]
    type: DocumentType
    created_at: datetime
    updated_at: datetime
