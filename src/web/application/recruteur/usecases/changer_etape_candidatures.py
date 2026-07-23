from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)


@dataclass
class CandidatureAChanger:
    candidature_id: UUID
    etape_actuelle_id: UUID


@dataclass
class ChangerEtapeCandidaturesCommand:
    organisme_id: UUID
    recrutement_id: UUID
    etape_cible_id: UUID
    candidatures: list[CandidatureAChanger]


@dataclass
class ChangerEtapeResultat:
    reussites: list[UUID]
    echecs: list[tuple[UUID, str]]  # (candidature_id, reason code)


# TODO: ajouter RBAC, validation de l'étape cible, détection de conflit
# mutation + sauvegarde
class ChangerEtapeCandidaturesUsecase(
    IUseCase[ChangerEtapeCandidaturesCommand, ChangerEtapeResultat]
):
    def __init__(self, organisme_repository: IOrganismeRepository):
        self.organisme_repository = organisme_repository

    def execute(self, command: ChangerEtapeCandidaturesCommand) -> ChangerEtapeResultat:
        self.organisme_repository.get_by_id(command.organisme_id)
        return ChangerEtapeResultat(
            reussites=[c.candidature_id for c in command.candidatures],
            echecs=[],
        )
