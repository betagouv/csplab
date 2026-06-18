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


class WebhookActionType(StrEnum):
    ARCHIVE = "archive"
    SAVE_RAW_OFFER = "save_raw_offer"


@dataclass(frozen=True)
class WebhookEvent:
    event_type: EventType
    reference: str
    status: OfferStatus | None = None

    def should_archive(self) -> bool:
        if self.event_type == EventType.SUPPRIME:
            return True
        return (
            self.event_type == EventType.STATUT_CHANGE
            and self.status != OfferStatus.DIFFUSE
        )

    def should_save_raw_offer(self) -> bool:
        return self.event_type in {EventType.CREE, EventType.MIS_A_JOUR}

    def get_action_type(self) -> WebhookActionType | None:
        if self.should_archive():
            return WebhookActionType.ARCHIVE
        if self.should_save_raw_offer():
            return WebhookActionType.SAVE_RAW_OFFER
        return None
