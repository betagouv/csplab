from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur
from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.repositories.candidature_recruteur_repository_interface import (
    ICandidatureRecruteurRepository,
)
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction

# les candidature dans le contexte d'un recruteur ont déjà la notion de _etape_id: UUID


@dataclass
class ChangerEtapeCandidaturesCommand:
    organisme_id: UUID
    recrutement_id: UUID
    utilisateur_id: UUID
    est_staff: bool
    etape_cible_id: UUID
    candidatures: list[UUID]  # list of CandidatureRecruteur


@dataclass
class ChangerEtapeResultat:
    reussites: list[UUID]
    echecs: list[tuple[UUID, str]]  # (candidature_id, reason code)


# TODO: ajouter
# - emission evenement + drain par auditlog
# - sauvegarde
class ChangerEtapeCandidaturesUsecase(
    IUseCase[ChangerEtapeCandidaturesCommand, ChangerEtapeResultat]
):
    def __init__(
        self,
        permission_service: OrganismePermissionService,
        organisme_recruteur_repository: IOrganismeRecruteurRepository,
        recrutement_repository: IRecrutementRepository,
        candidature_recruteur_repository: ICandidatureRecruteurRepository,
    ):
        self.permission_service = permission_service
        self.organisme_recruteur_repository = organisme_recruteur_repository
        self.recrutement_repository = recrutement_repository
        self.candidature_recruteur_repository = candidature_recruteur_repository

    def can_execute(
        self, command: ChangerEtapeCandidaturesCommand
    ) -> tuple[Recrutement, list[CandidatureRecruteur]]:
        recrutement = self.recrutement_repository.get_by_id(command.recrutement_id)
        candidatures = self.candidature_recruteur_repository.get_by_ids(
            command.candidatures
        )
        self.permission_service.est_autorise(
            action=OrganismeAction.CHANGER_ETAPE_CANDIDATURES,
            organisme_id=command.organisme_id,
            agent_id=command.utilisateur_id,
            est_staff=command.est_staff,
            recrutement_id=command.recrutement_id,
        )
        return recrutement, candidatures

    def execute(self, command: ChangerEtapeCandidaturesCommand) -> ChangerEtapeResultat:
        recrutement, candidatures = self.can_execute(command)
        successes, failures = recrutement.changer_etapes_candidatures(
            candidatures=candidatures, etape_cible_id=command.etape_cible_id
        )
        # todo: sauvegarder les changements d'etape
        return ChangerEtapeResultat(reussites=successes, echecs=failures)
