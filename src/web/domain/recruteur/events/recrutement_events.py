from dataclasses import dataclass
from uuid import UUID

from ddd.domain_event import DomainEvent

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement


@dataclass(frozen=True)
class RecrutementCree(DomainEvent):
    offre_id: UUID
    organisme_id: UUID
    etapes: tuple[EtapeRecrutement, ...]


@dataclass(frozen=True)
class EtapesAppliquees(DomainEvent):
    etapes: tuple[EtapeRecrutement, ...]


@dataclass(frozen=True)
class ResponsableAjoute(DomainEvent):
    agent_id: UUID


@dataclass(frozen=True)
class CandidatureRecue(DomainEvent):
    candidature_id: UUID


@dataclass(frozen=True)
class CandidatRecrute(DomainEvent):
    candidat_id: UUID
