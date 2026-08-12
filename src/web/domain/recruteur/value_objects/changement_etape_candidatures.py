from dataclasses import dataclass
from uuid import UUID

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur


@dataclass(frozen=True)
class ChangementEtapeCandidaturesResultat:
    reussites: list[CandidatureRecruteur]
    echecs: list[tuple[UUID, str]]
