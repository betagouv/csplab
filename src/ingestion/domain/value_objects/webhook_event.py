from dataclasses import dataclass
from enum import StrEnum


class EventType(StrEnum):
    CREE = "Cree"
    STATUT_CHANGE = "StatutChange"
    MIS_A_JOUR = "MisAJour"
    SUPPRIME = "Supprime"


class OfferStatus(StrEnum):
    ARCHIVE = "Archive"
    BROUILLON = "Brouillon"
    DIFFUSE = "Diffuse"
    EN_ATTENTE_PUBLICATION = "EnAttentePublication"
    FINALISE = "Finalise"
    SUSPENDUE = "Suspendue"
    VALIDE = "Valide"


@dataclass(frozen=True)
class WebhookEvent:
    event_type: EventType
    reference: str
    status: OfferStatus | None = None


def should_archive(event: WebhookEvent) -> bool:
    if event.event_type == EventType.SUPPRIME:
        return True
    return (
        event.event_type == EventType.STATUT_CHANGE
        and event.status != OfferStatus.DIFFUSE
    )


def should_save_raw_offer(event: WebhookEvent) -> bool:
    return event.event_type in {EventType.CREE, EventType.MIS_A_JOUR}
