from dataclasses import dataclass
from typing import List
from uuid import UUID

from ddd.domain_event import DomainEvent

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.value_objects.schema_etape_recrutement import (
    SchemaEtapeRecrutement,
)


@dataclass(frozen=True)
class ProcessusRecrutementReinitialise(DomainEvent):
    processus_recrutement: tuple[SchemaEtapeRecrutement, ...]


@dataclass(frozen=True)
class EtapesReordonnees(DomainEvent):
    etapes: tuple[EtapeRecrutement, ...]
    etapes_reordonnees: tuple[EtapeRecrutement, ...]


@dataclass(frozen=True)
class EtapeCandidaturesChangees(DomainEvent):
    candidatures: List[CandidatureRecruteur]
    etape_cible_id: UUID
