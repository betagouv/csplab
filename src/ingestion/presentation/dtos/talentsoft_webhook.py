from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class TalentsoftOfferStatus(StrEnum):
    ARCHIVE = "_TS_CO_OfferStatus_Archive"
    DIFFUSE = "_TS_CO_OfferStatus_Diffuse"
    EN_ATTENTE_PUBLICATION = "_TS_CO_OfferStatus_EnAttentePublication"
    FINALISE = "_TS_CO_OfferStatus_Finalise"
    SUSPENDUE = "_TS_CO_OfferStatus_Suspendue"
    VALIDE = "_TS_CO_OfferStatus_Valide"


class TalentsoftEventType(StrEnum):
    VACANCY_NEW = "vacancy_new"
    VACANCY_STATUS = "vacancy_status"
    VACANCY_UPDATE = "vacancy_update"
    VACANCY_DELETED = "vacancy_deleted"


class TalentsoftWebhookPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    event_type: str
    reference: str
    status_id: str | None = Field(None, alias="statusId")


def should_archive(payload: TalentsoftWebhookPayload) -> bool:
    if payload.event_type == TalentsoftEventType.VACANCY_DELETED:
        return True
    return (
        payload.event_type == TalentsoftEventType.VACANCY_STATUS
        and payload.status_id != TalentsoftOfferStatus.DIFFUSE
    )


def should_load_offer_details(payload: TalentsoftWebhookPayload) -> bool:
    return payload.event_type in {
        TalentsoftEventType.VACANCY_NEW,
        TalentsoftEventType.VACANCY_UPDATE,
    }
