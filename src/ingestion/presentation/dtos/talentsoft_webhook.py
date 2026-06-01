from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from domain.value_objects.webhook_event import EventType, OfferStatus, WebhookEvent


class TalentsoftEventType(StrEnum):
    VACANCY_NEW = "vacancy_new"
    VACANCY_STATUS = "vacancy_status"
    VACANCY_UPDATE = "vacancy_update"
    VACANCY_DELETED = "vacancy_deleted"


class TalentsoftOfferStatus(StrEnum):
    ARCHIVE = "_TS_CO_OfferStatus_Archive"
    DIFFUSE = "_TS_CO_OfferStatus_Diffuse"
    EN_ATTENTE_PUBLICATION = "_TS_CO_OfferStatus_EnAttentePublication"
    FINALISE = "_TS_CO_OfferStatus_Finalise"
    SUSPENDUE = "_TS_CO_OfferStatus_Suspendue"
    VALIDE = "_TS_CO_OfferStatus_Valide"


_EVENT_TYPE_MAP: dict[TalentsoftEventType, EventType] = {
    TalentsoftEventType.VACANCY_NEW: EventType.CREE,
    TalentsoftEventType.VACANCY_STATUS: EventType.STATUT_CHANGE,
    TalentsoftEventType.VACANCY_UPDATE: EventType.MIS_A_JOUR,
    TalentsoftEventType.VACANCY_DELETED: EventType.SUPPRIME,
}

_OFFER_STATUS_MAP: dict[TalentsoftOfferStatus, OfferStatus] = {
    TalentsoftOfferStatus.ARCHIVE: OfferStatus.ARCHIVE,
    TalentsoftOfferStatus.DIFFUSE: OfferStatus.DIFFUSE,
    TalentsoftOfferStatus.EN_ATTENTE_PUBLICATION: OfferStatus.EN_ATTENTE_PUBLICATION,
    TalentsoftOfferStatus.FINALISE: OfferStatus.FINALISE,
    TalentsoftOfferStatus.SUSPENDUE: OfferStatus.SUSPENDUE,
    TalentsoftOfferStatus.VALIDE: OfferStatus.VALIDE,
}


class TalentsoftWebhookPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    event_type: str
    reference: str
    status_id: str | None = Field(None, alias="statusId")

    def to_domain(self) -> WebhookEvent:
        event_type = _EVENT_TYPE_MAP[TalentsoftEventType(self.event_type)]
        status = (
            _OFFER_STATUS_MAP.get(TalentsoftOfferStatus(self.status_id))
            if self.status_id
            else None
        )
        return WebhookEvent(
            event_type=event_type,
            reference=self.reference,
            status=status,
        )
