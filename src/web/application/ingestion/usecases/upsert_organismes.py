from ddd.services.logger_interface import ILogger
from ddd.usecase_interface import IUseCase
from referentiel.entities.organisme import Organisme
from referentiel.types import IUpsertResult

from application.ingestion.interfaces.upsert_organismes_input import (
    OrganismeUpsertData,
    UpsertOrganismesInput,
)
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)


class UpsertOrganismesUsecase(IUseCase[UpsertOrganismesInput, IUpsertResult]):
    def __init__(
        self,
        organisme_repository: IOrganismeRepository,
        logger: ILogger,
    ):
        self.organisme_repository = organisme_repository
        self.logger = logger

    def execute(self, input_data: UpsertOrganismesInput) -> IUpsertResult:
        created = 0
        updated = 0
        errors: list = []

        for data in input_data.organismes:
            try:
                if self._upsert_one(data):
                    updated += 1
                else:
                    created += 1
            except Exception as e:
                errors.append(
                    {
                        "referentiel": data.referentiel,
                        "external_id": data.external_id,
                        "error": str(e),
                    }
                )

        self.logger.info(
            "UpsertOrganismes: created=%d updated=%d errors=%d",
            created,
            updated,
            len(errors),
        )
        return {"created": created, "updated": updated, "errors": errors}

    def _upsert_one(self, data: OrganismeUpsertData) -> bool:
        """Returns True if the organisme was updated, False if it was created."""
        existing = None
        if data.referentiel is not None and data.external_id is not None:
            existing = self.organisme_repository.get_by_referentiel_and_external_id(
                referentiel=data.referentiel, external_id=data.external_id
            )

        if existing is None:
            organisme = Organisme.create(
                nom=data.nom,
                versant=data.versant,
                localisation=data.localisation,
                siret=data.siret,
                parent_id=data.parent_id,
                external_id=data.external_id,
                referentiel=data.referentiel,
                millesime=data.millesime,
                gestion_ats=data.gestion_ats,
                date_creation=data.date_creation,
                date_derniere_activite=data.date_derniere_activite,
            )
            self.organisme_repository.create(organisme)
            return False

        existing.remplacer(
            nom=data.nom,
            versant=data.versant,
            localisation=data.localisation,
            siret=data.siret,
            parent_id=data.parent_id,
            external_id=data.external_id,
            referentiel=data.referentiel,
            millesime=data.millesime,
            gestion_ats=data.gestion_ats,
            date_creation=data.date_creation,
            date_derniere_activite=data.date_derniere_activite,
        )
        self.organisme_repository.save(existing)
        return True
