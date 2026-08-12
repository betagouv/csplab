from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur
from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.repositories.candidature_recruteur_repository_interface import (
    ICandidatureRecruteurRepository,
)
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.changement_etape_candidatures import (
    ChangementEtapeCandidaturesResultat,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction


@dataclass
class ChangerEtapeCandidaturesCommand:
    organisme_id: UUID
    recrutement_id: UUID
    utilisateur_id: UUID
    est_staff: bool
    etape_cible_id: UUID
    candidatures: list[UUID]


class ChangerEtapeCandidaturesUsecase(
    IUseCase[ChangerEtapeCandidaturesCommand, ChangementEtapeCandidaturesResultat]
):
    def __init__(
        self,
        permission_service: OrganismePermissionService,
        recrutement_repository: IRecrutementRepository,
        candidature_recruteur_repository: ICandidatureRecruteurRepository,
        audit_log_writer: AuditLogWriter,
    ):
        self.permission_service = permission_service
        self.recrutement_repository = recrutement_repository
        self.candidature_recruteur_repository = candidature_recruteur_repository
        self.audit_log_writer = audit_log_writer

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

    def execute(
        self, command: ChangerEtapeCandidaturesCommand
    ) -> ChangementEtapeCandidaturesResultat:
        recrutement, candidatures = self.can_execute(command)
        recrutement_modifie: ChangementEtapeCandidaturesResultat = (
            recrutement.changer_etapes_candidatures(
                candidatures=candidatures, etape_cible_id=command.etape_cible_id
            )
        )

        candidatures_traitees: ChangementEtapeCandidaturesResultat = (
            self.candidature_recruteur_repository.upsert(recrutement_modifie.reussites)
        )

        self.audit_log_writer.drain_events(
            utilisateur_id=command.utilisateur_id, aggregate=recrutement
        )
        return ChangementEtapeCandidaturesResultat(
            reussites=candidatures_traitees.reussites,
            echecs=recrutement_modifie.echecs + candidatures_traitees.echecs,
        )
