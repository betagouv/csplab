from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class DomainEventMetadata:
    aggregate_id: UUID
    aggregate: str
    event_name: str
    bounded_context: str | None = None
    version: int = 1


@dataclass(frozen=True, kw_only=True)
class DomainEvent:
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
    metadata: DomainEventMetadata | None = field(default=None)
