from dataclasses import dataclass
from typing import List

from ddd.usecase_interface import IUsecase

from application.identite.context_services.organisme_permission_service import (
    can_execute,
)
from application.recruteur.dtos.recrutement_request import RecrutementRequest
from application.recruteur.errors.application_errors_recruteur import (
    OrganismeRecrutementIncoherents,
    RecrutementEtapeIncoherents,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)
from domain.recruteur.value_objects.etape_data import EtapeData


@dataclass(kw_only=True)
class UpdateRecrutementEtapesCommand(RecrutementRequest):
    etapes_data: List[EtapeData]


class UpdateRecrutementEtapesUsecase(
    IUsecase[UpdateRecrutementEtapesCommand, tuple[EtapeRecrutement, ...]]
):
    def __init__(
        self,
        organisme_recruteur_repository: IOrganismeRecruteurRepository,
        recrutement_repository: IRecrutementRepository,
        audit_log_writer: AuditLogWriter,
    ):
        self.organisme_recruteur_repository = organisme_recruteur_repository
        self.recrutement_repository = recrutement_repository
        self.audit_log_writer = audit_log_writer

    def execute(
        self, command: UpdateRecrutementEtapesCommand
    ) -> tuple[EtapeRecrutement, ...]:
        self.organisme_recruteur_repository.get_by_id(command.organisme_id)
        recrutement = self.recrutement_repository.get_by_id(command.recrutement_id)
        if command.organisme_id != recrutement.organisme_id:
            raise OrganismeRecrutementIncoherents(
                command.organisme_id, command.recrutement_id
            )
        for config in command.etapes_data:
            if config.etape_uuid and config.etape_uuid not in [
                etape.entity_id for etape in recrutement.etapes
            ]:
                raise RecrutementEtapeIncoherents(
                    recrutement_id=recrutement.entity_id, etape_id=config.etape_uuid
                )

        can_execute(
            action=OrganismeAction.UPDATE_RECRUTEMENT_ETAPES,
            organisme_id=command.organisme_id,
            recrutement_id=command.recrutement_id,
            utilisateur=command.utilisateur,
        )

        recrutement.mettre_a_jour_etapes(etapes_data=tuple(command.etapes_data))
        self.recrutement_repository.save(recrutement)
        self.audit_log_writer.drain_events(
            utilisateur_id=command.utilisateur.entity_id, aggregate=recrutement
        )
        return recrutement.etapes
