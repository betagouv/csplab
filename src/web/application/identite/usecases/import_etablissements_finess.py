from ddd.domain_event import DomainEvent
from ddd.services.logger_interface import ILogger
from ddd.unit_of_work import IUnitOfWork
from ddd.usecase_interface import IUseCase
from referentiel.types import IUpsertResult

from domain.commons.constants import SYSTEM_UTILISATEUR_ID
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.organisme import Organisme
from domain.identite.errors.organisme_errors import EtablissementInvalideError
from domain.identite.events.organisme_events import OrganismeCree, OrganismeModifie
from domain.identite.gateways.organisme_gateway_interface import IOrganismeGateway
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
    IOrganismeUpsertResult,
)

BATCH_SIZE = 500


class ImportEtablissementsFinessUsecase(IUseCase[None, IUpsertResult]):
    def __init__(
        self,
        organisme_gateway: IOrganismeGateway,
        organisme_repository: IOrganismeRepository,
        logger: ILogger,
        unit_of_work: IUnitOfWork,
        audit_log_writer: AuditLogWriter,
    ):
        self.organisme_gateway = organisme_gateway
        self.organisme_repository = organisme_repository
        self.logger = logger
        self.unit_of_work = unit_of_work
        self.audit_log_writer = audit_log_writer

    def execute(self, input_data: None = None) -> IUpsertResult:
        resource = self.organisme_gateway.find_latest_resource()
        self.logger.info(
            "Import FINESS: fichier %s (millésime %s)",
            resource.url,
            resource.millesime.isoformat(),
        )

        result: IUpsertResult = {"created": 0, "updated": 0, "errors": []}
        batch: list[Organisme] = []

        organismes = self.organisme_gateway.stream_organismes(resource)
        while True:
            try:
                organisme = next(organismes)
            except StopIteration:
                break
            except EtablissementInvalideError as e:
                result["errors"].append(
                    {
                        "entity_id": e.external_id,
                        "error": str(e),
                        "exception": e,
                    }
                )
                continue

            batch.append(organisme)
            if len(batch) >= BATCH_SIZE:
                self._flush(batch, result)
                batch = []

        if batch:
            self._flush(batch, result)

        return result

    def _flush(self, batch: list[Organisme], result: IUpsertResult) -> None:
        with self.unit_of_work.atomic():
            batch_result: IOrganismeUpsertResult = (
                self.organisme_repository.upsert_batch(batch)
            )
        result["created"] += batch_result["created"]
        result["updated"] += batch_result["updated"]
        result["errors"].extend(batch_result["errors"])
        self._log_events(batch_result)

    def _log_events(self, batch_result: IOrganismeUpsertResult) -> None:
        for organisme in batch_result["created_organismes"]:
            self._drain_event(organisme, OrganismeCree)
        for organisme in batch_result["updated_organismes"]:
            self._drain_event(organisme, OrganismeModifie)

    def _drain_event(self, organisme: Organisme, event_type: type[DomainEvent]) -> None:
        organisme.add_event(
            event_type(
                aggregate_id=organisme.entity_id,
                aggregate=Organisme.__name__,
                event_name=event_type.__name__,
                nom=organisme.nom,
                versant=organisme.versant,
                localisation=organisme.localisation,
                siret=organisme.siret,
                parent_id=organisme.parent_id,
                external_id=organisme.external_id,
                referentiel=organisme.referentiel,
                millesime=organisme.millesime,
                gestion_ats=organisme.gestion_ats,
                date_creation=organisme.date_creation,
                date_derniere_activite=organisme.date_derniere_activite,
            )
        )
        self.audit_log_writer.drain_events(
            utilisateur_id=SYSTEM_UTILISATEUR_ID, aggregate=organisme
        )
