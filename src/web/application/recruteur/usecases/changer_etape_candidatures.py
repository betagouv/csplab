from dataclasses import dataclass
from typing import List
from uuid import UUID

from ddd.unit_of_work import IUnitOfWork
from ddd.usecase_interface import IUseCase
from referentiel.types import IBatchUpdate

from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur
from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.errors.recrutement_errors import RecrutementError
from domain.recruteur.repositories.candidature_recruteur_repository_interface import (
    ICandidatureRecruteurRepository,
)
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction


@dataclass
class ChangerEtapeCandidaturesCommand:
    organisme_id: UUID
    recrutement_id: UUID
    utilisateur_id: UUID
    est_staff: bool
    etape_cible_id: UUID
    candidatures: List[UUID]


class ChangerEtapeCandidaturesUsecase(
    IUseCase[
        ChangerEtapeCandidaturesCommand,
        IBatchUpdate[CandidatureRecruteur, RecrutementError],
    ]
):
    def __init__(
        self,
        permission_service: OrganismePermissionService,
        recrutement_repository: IRecrutementRepository,
        candidature_recruteur_repository: ICandidatureRecruteurRepository,
        audit_log_writer: AuditLogWriter,
        unit_of_work: IUnitOfWork,
    ):
        self.permission_service = permission_service
        self.recrutement_repository = recrutement_repository
        self.candidature_recruteur_repository = candidature_recruteur_repository
        self.audit_log_writer = audit_log_writer
        self.unit_of_work = unit_of_work

    def can_execute(
        self, command: ChangerEtapeCandidaturesCommand
    ) -> tuple[Recrutement, List[CandidatureRecruteur]]:
        recrutement = self.recrutement_repository.get_by_id(command.recrutement_id)
        candidatures_recruteur = self.candidature_recruteur_repository.get_by_ids(
            command.candidatures
        )
        self.permission_service.est_autorise(
            action=OrganismeAction.CHANGER_ETAPE_CANDIDATURES,
            organisme_id=command.organisme_id,
            agent_id=command.utilisateur_id,
            est_staff=command.est_staff,
            recrutement_id=command.recrutement_id,
        )
        return recrutement, candidatures_recruteur

    def execute(
        self, command: ChangerEtapeCandidaturesCommand
    ) -> IBatchUpdate[CandidatureRecruteur, RecrutementError]:
        with self.unit_of_work.atomic():
            recrutement, candidatures_recruteur = self.can_execute(command)
            recrutement_modifie: IBatchUpdate[
                CandidatureRecruteur, RecrutementError
            ] = recrutement.changer_etapes_candidatures(
                candidatures=candidatures_recruteur,
                etape_cible_id=command.etape_cible_id,
            )

            candidatures_traitees: IBatchUpdate[
                CandidatureRecruteur, RecrutementError
            ] = self.candidature_recruteur_repository.update_batch(
                recrutement_modifie["successes"]
            )

            self.audit_log_writer.drain_events(
                utilisateur_id=command.utilisateur_id, aggregate=recrutement
            )

            return {
                "successes": candidatures_traitees["successes"],
                "failures": recrutement_modifie["failures"]
                + candidatures_traitees["failures"],
            }
