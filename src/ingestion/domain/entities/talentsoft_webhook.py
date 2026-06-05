from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from domain.value_objects.webhook_event import EventType


@dataclass
class TalentsoftWebhook:
    source_id: str
    event_type: EventType
    reference: str
    payload: dict[str, Any]
    status_id: str | None = None
    id: UUID = field(default_factory=uuid4)
