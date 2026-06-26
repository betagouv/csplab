from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class ResponsableDTO:
    nom: str


@dataclass
class CandidaturesCountDTO:
    total: int | None
    a_traiter: int | None
    en_cours: int | None


@dataclass
class RecrutementDTO:  # base commune
    offer_id: UUID
    intitule: str
    reference_csp: str
    type_contrat: str | None
    type_offre: str | None
    date_publication: datetime
    responsables: list[ResponsableDTO]
    derniere_activite: datetime


@dataclass
class RecrutementActifDTO(RecrutementDTO):
    candidatures: CandidaturesCountDTO


@dataclass
class RecrutementArchiveDTO(RecrutementDTO):
    finalise: bool
    recrute: str | None


RecrutementItem = RecrutementActifDTO | RecrutementArchiveDTO


@dataclass
class PaginatedResult:
    total: int
    items: list[RecrutementItem] = field(default_factory=list)
