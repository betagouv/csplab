from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4


@dataclass
class RawOrganisme:
    referentiel: str
    millesime: str
    external_id: str
    data: Optional[dict[str, Any]] = None
    error_msg: Optional[str] = None
    loaded_at: Optional[datetime] = None
    cleaned_at: Optional[datetime] = None
    upsert_at: Optional[datetime] = None
    id: UUID = field(default_factory=uuid4)
