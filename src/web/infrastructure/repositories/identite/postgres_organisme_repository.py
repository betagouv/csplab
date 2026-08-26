from datetime import datetime
from typing import List
from uuid import UUID

from django.db import DatabaseError, transaction
from django.db.models import Q
from django.utils import timezone
from referentiel.entities.organisme import Organisme
from referentiel.types import IUpsertResult
from referentiel.value_objects.siret import SIRET

from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository as IOrganismeIdentiteRepository,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.mappers.organisme_identite_mapper import OrganismeIdentiteMapper


class PostgresOrganismeRepository(IOrganismeIdentiteRepository):
    def __init__(self) -> None:
        self._mapper_identite = OrganismeIdentiteMapper()

    def create(self, organisme: Organisme) -> Organisme:
        model = self._mapper_identite.from_domain(organisme)
        model.save()
        if organisme.date_creation:
            OrganismeModel.objects.filter(pk=model.pk).update(
                created_at=organisme.date_creation
            )
        return organisme

    def get_by_id(self, organisme_id: UUID) -> Organisme:  # type: ignore[override]
        try:
            model = OrganismeModel.objects.get(id=organisme_id)
        except OrganismeModel.DoesNotExist as e:
            raise OrganismeNexistePas(str(organisme_id)) from e
        return self._mapper_identite.to_domain(model)

    def get_by_siret(self, siret: SIRET) -> Organisme | None:
        try:
            model = OrganismeModel.objects.get(siret=str(siret))
        except OrganismeModel.DoesNotExist:
            return None
        return self._mapper_identite.to_domain(model)

    def save(self, organisme: Organisme) -> None:
        try:
            model = OrganismeModel.objects.get(id=organisme.entity_id)
        except OrganismeModel.DoesNotExist as e:
            raise OrganismeNexistePas(str(organisme.entity_id)) from e
        self._mapper_identite.apply_to_model(model, organisme)
        model.save()

    def get_all(self) -> List[Organisme]:
        return [
            self._mapper_identite.to_domain(model)
            for model in OrganismeModel.objects.all()
        ]

    def get_ids_by_referentiel_and_external_id(
        self, pairs: list[tuple[str, str]]
    ) -> dict[tuple[str, str], UUID]:
        if not pairs:
            return {}

        query = Q()
        for referentiel, external_id in pairs:
            query |= Q(referentiel=referentiel, external_id=external_id)

        models = OrganismeModel.objects.filter(query).only(
            "id", "referentiel", "external_id"
        )
        return {
            (str(model.referentiel), str(model.external_id)): model.id
            for model in models
        }

    def upsert_batch(self, organismes: list[Organisme]) -> IUpsertResult:
        try:
            with transaction.atomic():
                existing_ids = set(
                    OrganismeModel.objects.filter(
                        id__in=[organisme.entity_id for organisme in organismes]
                    )
                    .select_for_update(of=("self",))
                    .values_list("id", flat=True)
                )

                new_models = []
                models_to_update = []
                for organisme in organismes:
                    model = self._mapper_identite.from_domain(organisme)
                    if organisme.entity_id in existing_ids:
                        model.updated_at = timezone.make_aware(datetime.now())
                        models_to_update.append(model)
                    else:
                        new_models.append(model)

                created = 0
                if new_models:
                    created_models = OrganismeModel.objects.bulk_create(
                        new_models, ignore_conflicts=True
                    )
                    created = len(created_models)

                updated = 0
                if models_to_update:
                    updated = OrganismeModel.objects.bulk_update(
                        models_to_update,
                        fields=[
                            "nom",
                            "versant",
                            "siret",
                            "parent_id",
                            "localisation",
                            "external_id",
                            "referentiel",
                            "millesime",
                            "gestion_ats",
                            "date_creation",
                            "date_derniere_activite",
                            "updated_at",
                        ],
                    )

            return {"created": created, "updated": updated, "errors": []}
        except Exception as e:
            raise DatabaseError(f"Database error during bulk upsert: {e}") from e
