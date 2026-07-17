from dataclasses import dataclass
from uuid import UUID

from ddd.domain_event import DomainEvent


@dataclass(frozen=True)
class CandidatureRecue(DomainEvent):
    candidat_id: UUID
    etape_id: UUID
