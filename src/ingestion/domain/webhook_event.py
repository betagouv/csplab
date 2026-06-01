from dataclasses import dataclass
from enum import StrEnum


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


@dataclass(frozen=True)
class WebhookEvent:
    event_type: str
    reference: str
    status_id: str | None = None


def should_archive(event: WebhookEvent) -> bool:
    if event.event_type == TalentsoftEventType.VACANCY_DELETED:
        return True
    return (
        event.event_type == TalentsoftEventType.VACANCY_STATUS
        and event.status_id != TalentsoftOfferStatus.DIFFUSE
    )


def should_save_raw_offer(event: WebhookEvent) -> bool:
    return event.event_type in {
        TalentsoftEventType.VACANCY_NEW,
        TalentsoftEventType.VACANCY_UPDATE,
    }
