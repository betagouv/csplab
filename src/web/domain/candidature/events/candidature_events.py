from dataclasses import dataclass
from uuid import UUID

from domain.ddd.domain_event import DomainEvent


@dataclass(frozen=True)
class DossierCandidatureCree(DomainEvent):
    offre_id: UUID
    profil_candidat: UUID
    documents: tuple[UUID, ...]


@dataclass(frozen=True)
class DocumentsDeposes(DomainEvent):
    documents: tuple[UUID, ...]


@dataclass(frozen=True)
class CandidatureSoumise(DomainEvent):
    candidature_id: UUID


@dataclass(frozen=True)
class CandidatureRetiree(DomainEvent):
    candidature_id: UUID
