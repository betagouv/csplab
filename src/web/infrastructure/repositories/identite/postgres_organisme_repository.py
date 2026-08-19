from datetime import datetime
from typing import Dict, List
from uuid import UUID

from django.db import transaction
from django.utils import timezone
from referentiel.types import IUpsertError

from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.entities.organisme import Organisme
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository as IOrganismeIdentiteRepository,
)
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeUpsertResult,
)
from domain.identite.value_objects.siret import SIRET
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.exceptions.exceptions import DatabaseError
from infrastructure.mappers.organisme_identite_mapper import OrganismeIdentiteMapper

# Fields sourced from external referentials (e.g. FINESS): overwritten on
# upsert. parent_id is managed manually and never touched. gestion_ats is
# only set on creation: re-imports must not un-onboard an organisme that
# started managing its HR through the ATS in the meantime.
_UPSERT_UPDATE_FIELDS = [
    "nom",
    "versant",
    "localisation",
    "external_id",
    "referentiel",
    "millesime",
    "date_creation",
    "updated_at",
]


class PostgresOrganismeRepository(IOrganismeIdentiteRepository):
    def __init__(self) -> None:
        self._mapper_identite = OrganismeIdentiteMapper()

    def create(self, organisme: Organisme) -> Organisme:
        model = self._mapper_identite.from_domain(organisme)
        model.save()
        return organisme

    def get_by_id(self, organisme_id: UUID) -> Organisme:  # type: ignore[override]
        try:
            model = OrganismeModel.objects.get(id=organisme_id)
        except OrganismeModel.DoesNotExist as e:
            raise OrganismeNexistePas(str(organisme_id)) from e
        return self._mapper_identite.to_domain(model)

    def get_by_siret(self, siret: SIRET) -> Organisme:
        try:
            model = OrganismeModel.objects.get(siret=siret.value)
        except OrganismeModel.DoesNotExist as e:
            raise OrganismeNexistePas(siret.value) from e
        return self._mapper_identite.to_domain(model)

    def upsert_batch(self, organismes: List[Organisme]) -> IOrganismeUpsertResult:
        try:
            with transaction.atomic():
                existing_models = list(
                    OrganismeModel.objects.filter(
                        siret__in=[organisme.siret.value for organisme in organismes]
                    ).select_for_update(of=("self",))
                )
                existing_models_map: Dict[str, OrganismeModel] = {
                    model.siret: model for model in existing_models
                }

                partitioned: Dict[str, List[Organisme]] = {"new": [], "existing": []}
                for organisme in organismes:
                    if organisme.siret.value in existing_models_map:
                        partitioned["existing"].append(organisme)
                    else:
                        partitioned["new"].append(organisme)

                created = 0
                updated = 0

                if partitioned["new"]:
                    new_models = [
                        self._mapper_identite.from_domain(organisme)
                        for organisme in partitioned["new"]
                    ]
                    created_models = OrganismeModel.objects.bulk_create(
                        new_models, ignore_conflicts=True
                    )
                    created = len(created_models)

                if partitioned["existing"]:
                    models_to_update = []
                    for organisme in partitioned["existing"]:
                        existing_model = existing_models_map[organisme.siret.value]
                        updated_model = self._mapper_identite.from_domain(organisme)
                        updated_model.id = existing_model.id
                        updated_model.updated_at = timezone.make_aware(datetime.now())
                        models_to_update.append(updated_model)

                    updated = OrganismeModel.objects.bulk_update(
                        models_to_update, fields=_UPSERT_UPDATE_FIELDS
                    )

            errors: List[IUpsertError] = []
            result: IOrganismeUpsertResult = {
                "created": created,
                "updated": updated,
                "errors": errors,
                "created_organismes": partitioned["new"],
                "updated_organismes": partitioned["existing"],
            }
            return result

        except Exception as e:
            raise DatabaseError(
                "Database error during organisme bulk upsert", details={"error": str(e)}
            ) from e
