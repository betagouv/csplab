from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUsecase
from referentiel.entities.organisme import Organisme
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.identite.context_services.organisme_permission_service import (
    can_execute,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.errors.organisme_errors import OrganismeSiretExisteDeja
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.identite.value_objects.organisme_action import OrganismeAction


@dataclass
class CreateOrganismeCommand:
    localisation: Localisation | None
    parent_id: UUID | None
    name: str
    verse: Verse
    siret: SIRET
    utilisateur: Utilisateur
    managed_ats: bool = False


class CreateOrganismeUsecase(IUsecase[CreateOrganismeCommand, Organisme]):
    def __init__(
        self,
        organisme_repository: IOrganismeRepository,
        audit_log_writer: AuditLogWriter,
    ):
        self.organisme_repository = organisme_repository
        self.audit_log_writer = audit_log_writer

    def execute(self, command: CreateOrganismeCommand) -> Organisme:
        can_execute(
            action=OrganismeAction.CREER_ORGANISME,
            utilisateur=command.utilisateur,
        )
        organisme = self.organisme_repository.get_by_siret(siret=command.siret)
        if organisme:
            raise OrganismeSiretExisteDeja(siret_str=str(organisme.siret))
        organisme = Organisme.create(
            nom=command.name,
            versant=command.verse,
            localisation=command.localisation,
            siret=command.siret,
            parent_id=command.parent_id,
            gestion_ats=command.managed_ats,
        )
        self.audit_log_writer.drain_events(
            utilisateur_id=command.utilisateur.entity_id, aggregate=organisme
        )
        return self.organisme_repository.create(organisme)
