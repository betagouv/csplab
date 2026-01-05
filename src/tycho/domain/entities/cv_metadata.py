"""CVMetadata entity for CV storage and analysis."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict
from uuid import UUID

from domain.interfaces.entity_interface import IEntity


@dataclass
class CVMetadata(IEntity):
    """CVMetadata entity for storing CV information and extracted content."""

    id: UUID
    filename: str
    extracted_text: Dict[str, Any]
    search_query: str
    created_at: datetime
