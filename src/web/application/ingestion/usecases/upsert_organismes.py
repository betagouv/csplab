from uuid import UUID, uuid4

from ddd.services.logger_interface import ILogger
from ddd.usecase_interface import IUsecase
from referentiel.entities.organisme import Organisme
from referentiel.types import IUpsertError, IUpsertResult

from application.ingestion.interfaces.upsert_organismes_input import (
    OrganismeUpsertData,
    UpsertOrganismesInput,
)
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel


class UpsertOrganismesUsecase(IUsecase[UpsertOrganismesInput, IUpsertResult]):
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
        batch_ids = {pair: existing_ids.get(pair) or uuid4() for pair in pairs}
        known_ids = {
            **OrganismeModel.objects.ids_by_referentiel_and_external_id(
                [
                    (data.referentiel, data.parent_external_id)
                    for data in input_data.organismes
                    if data.parent_external_id
                ]
            ),
            **batch_ids,
        }

        organismes: list[Organisme] = []
        errors: list[IUpsertError] = []
        for data in input_data.organismes:
            pair = (data.referentiel, data.external_id)
            parent_id = None
            if data.parent_external_id:
                parent_id = known_ids.get((data.referentiel, data.parent_external_id))
                if parent_id is None:
                    errors.append(self._unknown_parent_error(data))
                    continue
            organismes.append(
                self._build_organisme(
                    data, batch_ids[pair], pair in existing_ids, parent_id
                )
            )

        result = self.organisme_repository.upsert_batch(organismes)
        result["errors"] = errors + result["errors"]
        self.logger.info(
            "UpsertOrganismes: created=%d updated=%d errors=%d",
            result["created"],
            result["updated"],
            len(result["errors"]),
        )
        return result

    @staticmethod
    def _unknown_parent_error(data: OrganismeUpsertData) -> IUpsertError:
        message = (
            f"parent_external_id {data.parent_external_id} inconnu "
            f"dans le référentiel {data.referentiel}"
        )
        return {"entity_id": None, "error": message, "exception": ValueError(message)}

    def _build_organisme(
        self,
        data: OrganismeUpsertData,
        entity_id: UUID,
        exists: bool,
        parent_id: UUID | None,
    ) -> Organisme:
        fields = {
            "nom": data.nom,
            "versant": data.versant,
            "localisation": data.localisation,
            "siret": data.siret,
            "parent_id": parent_id,
            "external_id": data.external_id,
            "referentiel": data.referentiel,
            "millesime": data.millesime,
            "gestion_ats": data.gestion_ats,
            "date_creation": data.date_creation,
            "date_derniere_activite": data.date_derniere_activite,
        }
        if not exists:
            return Organisme.create(entity_id=entity_id, **fields)

        organisme = Organisme.build(entity_id=entity_id, **fields)
        organisme.remplacer(**fields)
        return organisme
