from dataclasses import dataclass
from typing import List
from uuid import UUID

from ddd.domain_event import DomainEvent

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement


@dataclass(frozen=True)
class EtapesReinitialisees(DomainEvent):
    etapes_organisme: tuple[EtapeRecrutement, ...]


@dataclass(frozen=True)
class EtapeCandidaturesChangees(DomainEvent):
    candidatures: List[CandidatureRecruteur]
    etape_cible_id: UUID
