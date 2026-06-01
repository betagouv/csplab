from pydantic import BaseModel, ConfigDict, Field

from domain.webhook_event import WebhookEvent


class TalentsoftWebhookPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    event_type: str
    reference: str
    status_id: str | None = Field(None, alias="statusId")

    def to_domain(self) -> WebhookEvent:
        return WebhookEvent(
            event_type=self.event_type,
            reference=self.reference,
            status_id=self.status_id,
        )
