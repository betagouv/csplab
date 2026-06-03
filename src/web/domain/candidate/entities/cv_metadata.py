from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from ddd.entity import Entity
from ddd.types import JsonDataType

from domain.candidate.value_objects.cv_processing_status import CVStatus


@dataclass(kw_only=True)
class CVMetadata(Entity):
    entity_id: UUID
    filename: str
    status: CVStatus
    created_at: datetime
    updated_at: datetime
    extracted_text: Optional[JsonDataType] = None
    search_query: Optional[str] = None
