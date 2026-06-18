from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from domain.value_objects.webhook_event import EventType, WebhookActionType
from domain.value_objects.webhook_type import WebhookType


@dataclass
class Webhook:
    source_id: str
    event_type: EventType
    reference: str
    payload: dict[str, Any]
    webhook_type: WebhookType
    status_id: str | None = None
    action_type: WebhookActionType | None = None
    id: UUID = field(default_factory=uuid4)
