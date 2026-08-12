from dataclasses import dataclass
from uuid import UUID

from ddd.domain_event import DomainEvent

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur


@dataclass(frozen=True)
class EtapeCandidaturesChangees(DomainEvent):
    candidatures: list[CandidatureRecruteur]
    etape_cible_id: UUID
