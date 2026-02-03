"""CVMetadata entity for CV storage and analysis."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from domain.interfaces.entity_interface import IEntity
from domain.types import JsonDataType
from domain.value_objects.cv_processing_status import CVStatus


@dataclass
class CVMetadata(IEntity):
    """CVMetadata entity for storing CV information and extracted content."""

    id: UUID
    filename: str
    status: CVStatus
    created_at: datetime
    updated_at: datetime
    extracted_text: Optional[JsonDataType] = None
    search_query: Optional[str] = None
