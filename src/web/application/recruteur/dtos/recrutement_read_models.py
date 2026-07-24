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


@dataclass(frozen=True, kw_only=True)
class LocalisationDto:
    zone_geographique: str
    pays: str
    region: str
    departement: str
    localisation_label: str
    latitude: float | None
    longitude: float | None


@dataclass(frozen=True, kw_only=True)
class OrganismeRecruteurDto:
    nom: str
    siret: str


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
    intitule: str
    date_publication: datetime
    localisation: LocalisationDto
    organisme_recruteur: OrganismeRecruteurDto
    categorie_offre: str
    etapes: list[EtapeKanbanReadModel]
