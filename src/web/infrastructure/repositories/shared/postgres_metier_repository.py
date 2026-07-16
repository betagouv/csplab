from datetime import datetime
from typing import Dict, List

from ddd.page_interface import IPage
from ddd.services.logger_interface import ILogger
from django.db import DatabaseError, transaction
from django.db.models import F, Q
from django.utils import timezone
from referentiel.entities.metier import Metier
from referentiel.entities.offer import Offer
from referentiel.exceptions.metiers_error import MetierDoesNotExist
from referentiel.repositories.metier_repository_interface import IMetierRepository

from domain.ingestion.repositories.document_repository_interface import (
    IUpsertResult,
)
from infrastructure.django_apps.referentiel.models.metier import MetierModel
from infrastructure.mappers.metier_mapper import MetierMapper
from infrastructure.mappers.queryset_page_mapper import QuerySetPageMapper


class PostgresMetierRepository(IMetierRepository):
    def __init__(self, logger: ILogger, mapper: MetierMapper):
        self.logger = logger
        self.mapper = mapper

    def upsert_batch(self, metiers: List[Metier]) -> IUpsertResult:
        try:
            with transaction.atomic():
                existing_models = list(
                    MetierModel.objects.filter(
                        external_id__in=[metier.external_id for metier in metiers]
                    ).select_for_update(of=("self",))
                )

                existing_models_map = {
                    model.external_id: model for model in existing_models
                }
                existing_external_ids = set(existing_models_map.keys())

                partitioned: Dict[str, List[Metier]] = {"new": [], "existing": []}
                for metier in metiers:
                    if metier.external_id in existing_external_ids:
                        partitioned["existing"].append(metier)
                    else:
                        partitioned["new"].append(metier)

                created = 0
                updated = 0

                if partitioned["new"]:
                    new_models = []
                    for metier in partitioned["new"]:
                        model = self.mapper.from_domain(metier)
                        new_models.append(model)

                    created_models = MetierModel.objects.bulk_create(
                        new_models, ignore_conflicts=True
                    )
                    created = len(created_models)

                if partitioned["existing"]:
                    models_to_update = []
                    for metier in partitioned["existing"]:
                        if metier.external_id in existing_models_map:
                            existing_model = existing_models_map[metier.external_id]
                            updated_model = self.mapper.from_domain(metier)
                            updated_model.id = existing_model.id
                            updated_model.updated_at = timezone.make_aware(
                                datetime.now()
                            )
                            models_to_update.append(updated_model)

                    if models_to_update:
                        updated = MetierModel.objects.bulk_update(
                            models_to_update,
                            fields=[
                                "libelle_long",
                                "definition_synthetique",
                                "domaine_fonctionnel_code",
                                "offer_family_code",
                                "versants",
                                "activites",
                                "conditions_particulieres",
                                "updated_at",
                            ],
                        )

            return {"created": created, "updated": updated, "errors": []}

        except Exception as e:
            self.logger.error("Database error during bulk upsert: %s", str(e))
            raise DatabaseError("Database error during bulk upsert: %s", str(e)) from e

    def get_by_external_id(self, external_id: str) -> Metier:
        try:
            metier_model = MetierModel.objects.get(external_id=external_id)
            return self.mapper.to_domain(metier_model)
        except MetierModel.DoesNotExist as e:
            raise MetierDoesNotExist(
                f"Metier with external_id {external_id} not found"
            ) from e

    def get_all(self) -> List[Metier]:
        metier_models = MetierModel.objects.all()
        return [self.mapper.to_domain(model) for model in metier_models]

    def get_filtered_slice(self, predicate: Dict[str, str]) -> IPage[Metier]:
        qs = MetierModel.objects.filter(**predicate)
        return QuerySetPageMapper(
            qs.order_by("offer_family_code"), self.mapper.to_domain
        )

    def get_filtered(
        self, predicate: Dict[str, str], limit: int = 1000
    ) -> List[Metier]:
        metier_models = MetierModel.objects.filter(**predicate)[:limit]
        return [self.mapper.to_domain(model) for model in metier_models]

    def get_for_offer(self, offer: Offer) -> List[Metier]:
        if offer.family_code is None:
            self.logger.warning(
                "Offer with id %s has no family code, cannot fetch related metiers",
                offer.id,
            )
            return []
        return self.get_filtered({"offer_family_code": offer.family_code})

    @transaction.atomic
    def get_pending_processing(self, limit: int = 1000) -> List[Metier]:
        qs = (
            MetierModel.objects.filter(archived_at__isnull=True, processing=False)
            .filter(Q(processed_at__isnull=True) | Q(updated_at__gt=F("processed_at")))
            .select_for_update(of=("self",), skip_locked=True)[:limit]
        )

        for obj in qs:
            obj.processing = True
        try:
            MetierModel.objects.bulk_update(qs, ["processing"])
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e

        return [self.mapper.to_domain(model) for model in qs]

    def mark_as_processed(self, metiers_list: List[Metier]) -> int:
        try:
            return MetierModel.objects.filter(
                id__in=[obj.id for obj in metiers_list]
            ).update(processed_at=timezone.now(), processing=False)
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e

    def mark_as_pending(self, metiers_list: List[Metier]) -> int:
        try:
            return MetierModel.objects.filter(
                id__in=[obj.id for obj in metiers_list]
            ).update(processing=False)
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e
