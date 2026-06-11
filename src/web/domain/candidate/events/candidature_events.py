from dataclasses import dataclass
from uuid import UUID

from ddd.domain_event import DomainEvent


@dataclass(frozen=True)
class DossierCandidatureInitialise(DomainEvent):
    offre_id: UUID
    candidat_id: UUID


@dataclass(frozen=True)
class DocumentsDeposes(DomainEvent):
    documents: tuple[UUID, ...]


@dataclass(frozen=True)
class CandidatureSoumise(DomainEvent):
    pass
