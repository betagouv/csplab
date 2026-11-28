from typing import List
from uuid import UUID

from ddd.page_interface import IPage
from ddd.services.logger_interface import ILogger
from django.db import DatabaseError, transaction
from django.db.models import F, Q, prefetch_related_objects
from django.utils import timezone
from referentiel.entities.offer import Offer
from referentiel.exceptions.offer_errors import (
    MultipleOffersFoundForReference,
    OfferDoesNotExist,
)
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.offer_conditions import Management, WorkingPlace
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from domain.ingestion.repositories.ingestion_offers_repository_interface import (
    IIngestionOffersRepository,
)
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.mappers.offer_mapper import OfferMapper
from infrastructure.mappers.queryset_page import QuerySetPage


class PostgresOffersRepository(IIngestionOffersRepository):
    def __init__(self, logger: ILogger, mapper: OfferMapper):
        self.logger = logger
        self.mapper = mapper

    def get_by_id(self, offer_id: UUID) -> Offer:
        try:
            offer_model = OfferModel.objects.with_localisations().get(id=offer_id)
            return self.mapper.to_domain(offer_model)
        except OfferModel.DoesNotExist as e:
            raise OfferDoesNotExist(offer_id) from e

    def get_by_ids(self, offer_ids: List[UUID]) -> List[Offer]:
        offers = OfferModel.objects.with_localisations().filter(id__in=offer_ids)
        return [self.mapper.to_domain(offer) for offer in offers]

    def get_by_reference_and_source_id(self, reference: str, source_id: UUID) -> Offer:
        try:
            offer_model = OfferModel.objects.with_localisations().get(
                reference=reference, source_id=source_id
            )
            return self.mapper.to_domain(offer_model)
        except OfferModel.DoesNotExist as e:
            raise OfferDoesNotExist(reference) from e

    def get_by_reference(self, reference: str) -> Offer:
        try:
            offer_model = (
                OfferModel.objects.select_related("talentsoft_organisme_entity_code")
                .with_localisations()
                .get(reference=reference)
            )
        except OfferModel.DoesNotExist as e:
            raise OfferDoesNotExist(reference) from e
        except OfferModel.MultipleObjectsReturned as e:
            raise MultipleOffersFoundForReference(reference) from e
        return self.mapper.to_domain(offer_model)

    def get_all(self) -> List[Offer]:
        offer_models = OfferModel.objects.with_localisations()
        return [self.mapper.to_domain(model) for model in offer_models]

    def get_filtered(
        self,
        active: bool,
        category: List[Category] | None = None,
        verse: List[Verse] | None = None,
        offer_nature: List[OfferNature] | None = None,
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
        qs = (
            OfferModel.objects.select_related("talentsoft_organisme_entity_code")
            .with_localisations()
            .filtered(
                active=active,
                category=category,
                verse=verse,
                offer_nature=offer_nature,
                experience_level=experience_level,
                management=management,
                working_place=working_place,
                region=region,
                department=department,
                country=country,
                area=area,
                domain=domain,
                organization=organization,
                published_within_days=published_within_days,
                latitude=latitude,
                longitude=longitude,
                radius_km=radius_km,
                keywords=keywords,
            )
        )
        return QuerySetPage(qs, self.mapper.to_domain)

    def get_by_source_id(self, source_id: UUID) -> IPage[Offer]:
        qs = OfferModel.objects.with_localisations().filter(
            source_id=source_id, archived_at__isnull=True
        )
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

        models = list(qs)
        prefetch_related_objects(models, "localisations")
        return [self.mapper.to_domain(model) for model in models]

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
