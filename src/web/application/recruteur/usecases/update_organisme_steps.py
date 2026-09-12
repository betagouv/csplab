from dataclasses import dataclass
from typing import List
from uuid import UUID

from ddd.usecase_interface import IUsecase

from application.identite.context_services.organisme_permission_service import (
    can_execute,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.value_objects.etape_data import EtapeData


@dataclass
class UpdateOrganismeStepsCommand:
    organisme_id: UUID
    utilisateur: Utilisateur
    etapes: List[EtapeData]


class UpdateOrganismeStepsUsecase(
    IUsecase[UpdateOrganismeStepsCommand, OrganismeRecruteur]
):
    def __init__(
        self,
        organisme_recruteur_repository: IOrganismeRecruteurRepository,
        audit_log_writer: AuditLogWriter,
    ):
        self.organisme_recruteur_repository = organisme_recruteur_repository
        self.audit_log_writer = audit_log_writer

    def execute(self, command: UpdateOrganismeStepsCommand) -> OrganismeRecruteur:
        can_execute(
            action=OrganismeAction.UPDATE_ORGANISME_STEPS,
            organisme_id=command.organisme_id,
            utilisateur=command.utilisateur,
        )
        organisme_recruteur = self.organisme_recruteur_repository.get_by_id(
            command.organisme_id
        )

        organisme_recruteur.mettre_a_jour_etapes(etapes_data=tuple(command.etapes))
        self.organisme_recruteur_repository.save(organisme_recruteur)
        self.audit_log_writer.drain_events(
            utilisateur_id=command.utilisateur.entity_id, aggregate=organisme_recruteur
        )
        return organisme_recruteur
