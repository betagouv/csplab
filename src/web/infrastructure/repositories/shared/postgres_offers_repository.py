import operator
from datetime import datetime, timedelta
from functools import reduce
from typing import Dict, List
from uuid import UUID

from ddd.page_interface import IPage
from ddd.services.logger_interface import ILogger
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db import DatabaseError, transaction
from django.db.models import F, FloatField, Q, Value
from django.db.models.functions import ACos, Cos, Greatest, Least, Radians, Sin
from django.utils import timezone
from referentiel.entities.offer import Offer
from referentiel.exceptions.offer_errors import OfferDoesNotExist
from referentiel.types import IUpsertResult
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.offer_conditions import Management, WorkingPlace
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from domain.ingestion.repositories.ingestion_offers_repository_interface import (
    IIngestionOffersRepository,
)
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.mappers.offer_mapper import OfferMapper
from infrastructure.mappers.queryset_page import QuerySetPage

EARTH_RADIUS_KM = 6371.0
SEARCH_CONFIG = "french"
KEYWORDS_SEARCH_WEIGHTS = {
    "A": ("title",),
    "B": ("long_title",),
    "C": ("mission", "profile", "organization", "employer", "complements"),
}


class PostgresOffersRepository(IIngestionOffersRepository):
    def __init__(self, logger: ILogger, mapper: OfferMapper):
        self.logger = logger
        self.mapper = mapper

    def upsert_batch(self, offers_list: List[Offer]) -> IUpsertResult:
        try:
            with transaction.atomic():
                existing_models = list(
                    OfferModel.objects.filter(
                        external_id__in=[offer.external_id for offer in offers_list]
                    ).select_for_update(of=("self",))
                )

                existing_models_map = {
                    model.external_id: model for model in existing_models
                }
                existing_external_ids = set(existing_models_map.keys())

                partitioned: Dict[str, List[Offer]] = {"new": [], "existing": []}
                for offer in offers_list:
                    if offer.external_id in existing_external_ids:
                        partitioned["existing"].append(offer)
                    else:
                        partitioned["new"].append(offer)

                created = 0
                updated = 0

                if partitioned["new"]:
                    new_models = []
                    for offer in partitioned["new"]:
                        model = self.mapper.from_domain(offer)
                        new_models.append(model)

                    created_models = OfferModel.objects.bulk_create(
                        new_models, ignore_conflicts=True
                    )
                    created = len(created_models)

                if partitioned["existing"]:
                    models_to_update = []
                    for offer in partitioned["existing"]:
                        if offer.external_id in existing_models_map:
                            existing_model = existing_models_map[offer.external_id]
                            updated_model = self.mapper.from_domain(offer)
                            updated_model.id = existing_model.id
                            updated_model.updated_at = timezone.make_aware(
                                datetime.now()
                            )
                            models_to_update.append(updated_model)

                    if models_to_update:
                        updated = OfferModel.objects.bulk_update(
                            models_to_update,
                            fields=[
                                "reference",
                                "verse",
                                "title",
                                "profile",
                                "mission",
                                "category",
                                "contract_type",
                                "organization",
                                "offer_url",
                                "code_emploi_csp",
                                "job_family_referential",
                                "local_job_code",
                                "functional_area_code",
                                "area",
                                "country",
                                "region",
                                "department",
                                "location_label",
                                "latitude",
                                "longitude",
                                "publication_date",
                                "beginning_date",
                                "updated_at",
                                "archived_at",
                                "long_title",
                                "application_url",
                                "contract_kind",
                                "job_vacancy",
                                "employer",
                                "complements",
                                "criteria",
                                "conditions",
                                "contacts",
                            ],
                        )

            return {"created": created, "updated": updated, "errors": []}

        except Exception as e:
            self.logger.error("Database error during bulk upsert: %s", str(e))
            raise DatabaseError("Database error during bulk upsert: %s", str(e)) from e

    def get_by_id(self, offer_id: UUID) -> Offer:
        try:
            offer_model = OfferModel.objects.get(id=offer_id)
            return self.mapper.to_domain(offer_model)
        except OfferModel.DoesNotExist as e:
            raise OfferDoesNotExist(offer_id) from e

    def get_by_ids(self, offer_ids: List[UUID]) -> List[Offer]:
        offers = OfferModel.objects.filter(id__in=offer_ids)
        return [self.mapper.to_domain(offer) for offer in offers]

    def get_by_external_id(self, external_id: str) -> Offer:
        try:
            offer_model = OfferModel.objects.get(external_id=external_id)
            return self.mapper.to_domain(offer_model)
        except OfferModel.DoesNotExist as e:
            raise OfferDoesNotExist(external_id) from e

    def get_by_reference_and_source_id(self, reference: str, source_id: UUID) -> Offer:
        try:
            offer_model = OfferModel.objects.get(
                reference=reference, source_id=source_id
            )
            return self.mapper.to_domain(offer_model)
        except OfferModel.DoesNotExist as e:
            raise OfferDoesNotExist(reference) from e

    def get_by_external_ids(self, external_ids: List[str]) -> List[Offer]:
        offers = OfferModel.objects.filter(external_id__in=external_ids)
        return [self.mapper.to_domain(offer) for offer in offers]

    def get_all(self) -> List[Offer]:
        offer_models = OfferModel.objects.all()
        return [self.mapper.to_domain(model) for model in offer_models]

    def get_filtered(
        self,
        active: bool,
        external_id_contains: str | None,
        category: List[Category] | None = None,
        verse: List[Verse] | None = None,
        contract_type: List[ContractType] | None = None,
        experience_level: List[ExperienceLevel] | None = None,
        management: List[Management] | None = None,
        working_place: List[WorkingPlace] | None = None,
        region: List[Region] | None = None,
        department: List[Department] | None = None,
        country: List[Country] | None = None,
        area: List[GeographicalArea] | None = None,
        domain: List[str] | None = None,
        organization: List[str] | None = None,
        published_within_days: int | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        radius_km: int | None = None,
        keywords: str | None = None,
    ) -> IPage[Offer]:
        qs = OfferModel.objects.filter(archived_at__isnull=active)

        if external_id_contains:
            qs = qs.filter(external_id__contains=external_id_contains)

        qs = self._apply_field_filters(
            qs,
            [
                ("category__in", category, lambda c: c.value),
                ("verse__in", verse, lambda v: v.value),
                ("contract_type__in", contract_type, lambda c: c.value),
                ("criteria__experience__in", experience_level, lambda e: e.name),
                ("conditions__management__in", management, lambda m: m.name),
                (
                    "conditions__lieu_de_travail__in",
                    working_place,
                    lambda w: w.name,
                ),
                ("region__in", region, lambda r: r.code),
                ("department__in", department, lambda d: d.code),
                ("country__in", country, str),
                ("area__in", area, lambda a: a.value),
                ("functional_area_code__in", domain, str),
                ("organization__in", organization, str),
            ],
        )

        if published_within_days is not None:
            since = timezone.now() - timedelta(days=abs(published_within_days))
            qs = qs.filter(publication_date__gte=since)

        if latitude is not None and longitude is not None and radius_km is not None:
            qs = self._filter_by_radius(qs, latitude, longitude, radius_km)

        if keywords:
            qs = self._filter_by_keywords(qs, keywords)
            qs = qs.order_by("-rank", "-updated_at")
        else:
            qs = qs.order_by("-updated_at")

        return QuerySetPage(qs, self.mapper.to_domain)

    @staticmethod
    def _apply_field_filters(qs, filters):
        for lookup, values, transform in filters:
            if values:
                qs = qs.filter(**{lookup: [transform(v) for v in values]})
        return qs

    def _filter_by_radius(self, qs, latitude: float, longitude: float, radius_km: int):
        qs = qs.filter(latitude__isnull=False, longitude__isnull=False)
        distance_km = EARTH_RADIUS_KM * ACos(
            Least(
                Value(1.0, output_field=FloatField()),
                Greatest(
                    Value(-1.0, output_field=FloatField()),
                    Cos(Radians(Value(latitude, output_field=FloatField())))
                    * Cos(Radians(F("latitude")))
                    * Cos(
                        Radians(F("longitude"))
                        - Radians(Value(longitude, output_field=FloatField()))
                    )
                    + Sin(Radians(Value(latitude, output_field=FloatField())))
                    * Sin(Radians(F("latitude"))),
                ),
            )
        )
        return qs.annotate(distance_km=distance_km).filter(distance_km__lte=radius_km)

    @staticmethod
    def _filter_by_keywords(qs, keywords: str):
        vectors = [
            SearchVector(*fields, weight=weight, config=SEARCH_CONFIG)
            for weight, fields in KEYWORDS_SEARCH_WEIGHTS.items()
        ]
        search_vector = reduce(operator.add, vectors)
        search_query = SearchQuery(keywords, config=SEARCH_CONFIG)
        return qs.annotate(
            search=search_vector, rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query)

    def get_by_source_id(self, source_id: UUID) -> IPage[Offer]:
        qs = OfferModel.objects.filter(source_id=source_id, archived_at__isnull=True)
        return QuerySetPage(qs.order_by("-updated_at"), self.mapper.to_domain)

    @transaction.atomic
    def get_pending_processing(self, limit: int = 1000) -> List[Offer]:
        qs = (
            OfferModel.objects.filter(archived_at__isnull=True, processing=False)
            .filter(Q(processed_at__isnull=True) | Q(updated_at__gt=F("processed_at")))
            .select_for_update(of=("self",), skip_locked=True)[:limit]
        )

        for obj in qs:
            obj.processing = True
        try:
            OfferModel.objects.bulk_update(qs, ["processing"])
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e

        return [self.mapper.to_domain(model) for model in qs]

    def mark_as_processed(self, offers_list: List[Offer]) -> int:
        try:
            return OfferModel.objects.filter(
                id__in=[obj.id for obj in offers_list]
            ).update(processed_at=timezone.now(), processing=False)
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e

    def mark_as_pending(self, offers_list: List[Offer]) -> int:
        try:
            return OfferModel.objects.filter(
                id__in=[obj.id for obj in offers_list]
            ).update(processing=False)
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e

    def mark_as_archived(self, offers_list: List[Offer]) -> int:
        try:
            return OfferModel.objects.filter(
                archived_at__isnull=True, id__in=[obj.id for obj in offers_list]
            ).update(archived_at=timezone.now())
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e
