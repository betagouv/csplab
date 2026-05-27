from pydantic import BaseModel, ConfigDict, Field

_TS_ARCHIVED = "_TS_CO_OfferStatus_Archive"

_VACANCY_LOAD_EVENT_TYPES = {"vacancy_new", "vacancy_update"}


class TalentsoftWebhookPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    event_type: str
    reference: str
    status_id: str | None = Field(None, alias="statusId")


def should_archive(payload: TalentsoftWebhookPayload) -> bool:
    if payload.event_type == "vacancy_deleted":
        return True
    return payload.event_type == "vacancy_status" and payload.status_id == _TS_ARCHIVED


def should_load_offer_details(payload: TalentsoftWebhookPayload) -> bool:
    return payload.event_type in _VACANCY_LOAD_EVENT_TYPES
