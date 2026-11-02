from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, kw_only=True)
class CandidatDto:
    uuid: UUID
    nom: str
    prenom: str


@dataclass(frozen=True, kw_only=True)
class EtapeDto:
    etape_uuid: UUID
    nom: str
    categorie: str


@dataclass(frozen=True, kw_only=True)
class CandidatureKanbanDto:
    uuid: UUID
    date_soumission: datetime
    date_derniere_activite: datetime
    candidat: CandidatDto


@dataclass(frozen=True, kw_only=True)
class EtapeKanbanReadModel:
    etape_uuid: UUID
    nom: str
    categorie: str
    candidatures: list[CandidatureKanbanDto]


@dataclass(frozen=True, kw_only=True)
class RecrutementKanbanReadModel:
    offer_id: UUID
    etapes: list[EtapeKanbanReadModel]
