from uuid import UUID

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
        pairs = [(data.referentiel, data.external_id) for data in input_data.organismes]
        existing_ids = self.organisme_repository.get_ids_by_referentiel_and_external_id(
            pairs
        )

        organismes = [
            self._build_organisme(
                data, existing_ids.get((data.referentiel, data.external_id))
            )
            for data in input_data.organismes
        ]

        result = self.organisme_repository.upsert_batch(organismes)
        self.logger.info(
            "UpsertOrganismes: created=%d updated=%d errors=%d",
            result["created"],
            result["updated"],
            len(result["errors"]),
        )
        return result

    def _build_organisme(
        self, data: OrganismeUpsertData, existing_id: UUID | None
    ) -> Organisme:
        fields = {
            "nom": data.nom,
            "versant": data.versant,
            "localisation": data.localisation,
            "siret": data.siret,
            "parent_id": data.parent_id,
            "external_id": data.external_id,
            "referentiel": data.referentiel,
            "millesime": data.millesime,
            "gestion_ats": data.gestion_ats,
            "date_creation": data.date_creation,
            "date_derniere_activite": data.date_derniere_activite,
        }
        if existing_id is None:
            return Organisme.create(**fields)

        organisme = Organisme.build(entity_id=existing_id, **fields)
        organisme.remplacer(**fields)
        return organisme
