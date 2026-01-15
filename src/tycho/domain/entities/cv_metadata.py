"""CVMetadata entity for CV storage and analysis."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.interfaces.entity_interface import IEntity
from domain.types import JsonDataType


@dataclass
class CVMetadata(IEntity):
    """CVMetadata entity for storing CV information and extracted content."""

    id: UUID
    filename: str
    extracted_text: JsonDataType
    search_query: str
    created_at: datetime
