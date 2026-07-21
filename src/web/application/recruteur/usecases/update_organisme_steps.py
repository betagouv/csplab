from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction


@dataclass
class EtapeData:
    etape_uuid: UUID | None
    nom: str
    categorie: CategorieEtapeRecrutement


@dataclass
class UpdateOrganismeStepsCommand:
    organisme_id: UUID
    utilisateur_id: UUID
    etapes: list[EtapeData]
    est_staff: bool = False


class UpdateOrganismeStepsUsecase(
    IUseCase[UpdateOrganismeStepsCommand, OrganismeRecruteur]
):
    def __init__(
        self,
        organisme_repository: IOrganismeRepository,
        organisme_recruteur_repository: IOrganismeRecruteurRepository,
        audit_log_writer: AuditLogWriter,
        organisme_permission_service: OrganismePermissionService,
    ):
        self.organisme_repository = organisme_repository
        self.organisme_recruteur_repository = organisme_recruteur_repository
        self.audit_log_writer = audit_log_writer
        self.organisme_permission_service = organisme_permission_service

    def execute(self, command: UpdateOrganismeStepsCommand) -> OrganismeRecruteur:
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.UPDATE_ORGANISME_STEPS,
            organisme_id=command.organisme_id,
            agent_id=command.utilisateur_id,
            est_staff=command.est_staff,
        )
        # guard, raise OrganismeInexistant if not found
        self.organisme_repository.get_by_id(command.organisme_id)
        organisme_recruteur = self.organisme_recruteur_repository.get_by_id(
            command.organisme_id
        )

        etapes = tuple(
            EtapeRecrutement.build(
                entity_id=etape_data.etape_uuid,
                categorie=etape_data.categorie,
                nom=etape_data.nom,
            )
            if etape_data.etape_uuid is not None
            else EtapeRecrutement.create(
                categorie=etape_data.categorie,
                nom=etape_data.nom,
            )
            for etape_data in command.etapes
        )

        # todo with atomic transaction in the repository
        organisme_recruteur.mettre_a_jour_etapes(etapes=etapes)
        self.organisme_recruteur_repository.save(organisme_recruteur)
        self.audit_log_writer.drain_events(
            utilisateur_id=command.utilisateur_id, aggregate=organisme_recruteur
        )
        return organisme_recruteur
