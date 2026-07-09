from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, kw_only=True)
class ResponsableDto:
    nom: str


@dataclass(frozen=True, kw_only=True)
class CandidaturesCompteurDto:
    total: int
    a_traiter: int
    en_cours: int


@dataclass(frozen=True, kw_only=True)
class RecrutementActifsReadModel:
    offer_id: UUID
    intitule: str
    reference_csp: str
    type_contrat: str
    date_publication: datetime
    responsables: list[ResponsableDto]
    derniere_activite: datetime
    candidatures: CandidaturesCompteurDto


@dataclass(frozen=True, kw_only=True)
class RecrutementArchivesReadModel:
    offer_id: UUID
    intitule: str
    reference_csp: str
    type_contrat: str
    date_archivage: datetime
    responsables: list[ResponsableDto]
    finalise: bool
    recrute: str | None
