from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ddd.entity import Entity


@dataclass(kw_only=True)
class AuditLog(Entity):
    event_id: UUID | None
    occurred_at: datetime
    utilisateur_id: UUID
    ressource_kind: str
    ressource_id: UUID
    event_name: str
