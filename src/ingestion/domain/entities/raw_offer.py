from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4


@dataclass
class RawOffer:
    reference: str
    source_id: str | None = None
    data: Optional[dict[str, Any]] = None
    error_msg: Optional[str] = None
    loaded_at: Optional[datetime] = None
    cleaned_at: Optional[datetime] = None
    upsert_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None
    id: UUID = field(default_factory=uuid4)
