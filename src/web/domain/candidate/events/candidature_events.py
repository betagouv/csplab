from dataclasses import dataclass
from uuid import UUID

from ddd.domain_event import DomainEvent


@dataclass(frozen=True)
class DossierCandidatureCree(DomainEvent):
    offre_id: UUID
    profil_candidat_id: UUID


@dataclass(frozen=True)
class DocumentsDeposes(DomainEvent):
    documents: tuple[UUID, ...]


@dataclass(frozen=True)
class CandidatureSoumise(DomainEvent):
    pass
