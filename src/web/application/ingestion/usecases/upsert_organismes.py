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
        new_pairs = set(pairs) - existing_ids.keys()
        existing_parent_ids = (
            OrganismeModel.objects.not_supprimes().ids_by_referentiel_and_external_id(
                [
                    (data.referentiel, data.parent_external_id)
                    for data in input_data.organismes
                    if data.parent_external_id
                ]
            )
        )

        errors: list[IUpsertError] = []
        accepted: list[OrganismeUpsertData] = []
        seen: set[tuple[str, str]] = set()
        for data in input_data.organismes:
            pair = (data.referentiel, data.external_id)
            if pair in seen:
                errors.append(
                    self._error(
                        f"{data.referentiel} {data.external_id} en double dans le lot"
                    )
                )
                continue
            seen.add(pair)
            accepted.append(data)

        rejected: set[tuple[str, str]] = set()
        while rejected_now := {
            (data.referentiel, data.external_id): message
            for data in accepted
            if (
                message := self._parent_error(
                    data, new_pairs, rejected, existing_parent_ids
                )
            )
        }:
            errors.extend(self._error(message) for message in rejected_now.values())
            rejected |= rejected_now.keys()
            accepted = [
                data
                for data in accepted
                if (data.referentiel, data.external_id) not in rejected_now
            ]

        organismes: list[Organisme] = []
        for data in accepted:
            pair = (data.referentiel, data.external_id)
            parent_id = None
            if data.parent_external_id:
                parent_pair = (data.referentiel, data.parent_external_id)
                parent_id = (
                    existing_parent_ids.get(parent_pair) or batch_ids[parent_pair]
                )
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
    def _parent_error(
        data: OrganismeUpsertData,
        new_pairs: set[tuple[str, str]],
        rejected: set[tuple[str, str]],
        existing_parent_ids: dict[tuple[str, str], UUID],
    ) -> str | None:
        if not data.parent_external_id:
            return None
        parent_pair = (data.referentiel, data.parent_external_id)
        if parent_pair in rejected and parent_pair not in existing_parent_ids:
            return (
                f"parent de {data.referentiel} {data.external_id} "
                "rejeté dans le même lot"
            )
        if data.parent_external_id == data.external_id or (
            parent_pair not in new_pairs and parent_pair not in existing_parent_ids
        ):
            return (
                f"parent_external_id {data.parent_external_id} inconnu "
                f"dans le référentiel {data.referentiel}"
            )
        return None

    @staticmethod
    def _error(message: str) -> IUpsertError:
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
