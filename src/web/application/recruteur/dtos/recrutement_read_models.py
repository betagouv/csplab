from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, kw_only=True)
class AgentDto:
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
    agents: list[AgentDto]
    derniere_activite: datetime
    candidatures: CandidaturesCompteurDto


@dataclass(frozen=True, kw_only=True)
class RecrutementArchivesReadModel:
    offer_id: UUID
    intitule: str
    reference_csp: str
    type_contrat: str
    date_archivage: datetime
    agents: list[AgentDto]
    finalise: bool
    recrute: str | None


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
class CandidatureListeReadModel:
    uuid: UUID
    date_soumission: datetime
    date_derniere_activite: datetime
    candidat: CandidatDto
    etape: EtapeDto
