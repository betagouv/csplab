from datetime import UTC, datetime
from typing import List, Optional
from uuid import uuid4

from django.utils import timezone
from pydantic import HttpUrl

from domain.entities.offer import Offer
from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
from domain.value_objects.country import Country
from domain.value_objects.department import Department
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.region import Region
from domain.value_objects.verse import Verse
from infrastructure.django_apps.shared.models.offer import OfferModel


class OfferFactory:
    @staticmethod
    def build(
        title: str = "Test Offer Title",
        department: str = "75",
        category: Category = Category.A,
        verse: Verse = Verse.FPE,
        external_id: str | None = None,
        profile: str = "Test profile description",
        mission: str = "Test mission description",
        organization: str = "Test Organization",
        localisation: Localisation | None = None,
    ) -> Offer:
        return Offer(
            external_id=external_id or f"OFFER_{uuid4().hex[:8]}",
            verse=verse,
            title=title,
            profile=profile,
            mission=mission,
            category=category,
            contract_type=None,
            organization=organization,
            offer_url=None,
            localisation=localisation
            or Localisation(
                country=Country("FRA"),
                region=Region(code="11"),
                department=Department(code=department),
            ),
            publication_date=datetime(2024, 1, 15, tzinfo=UTC),
            beginning_date=LimitDate(datetime(2024, 12, 31, tzinfo=UTC)),
            processed_at=None,
            archived_at=None,
        )

    @staticmethod
    def create(
        external_id: Optional[str] = None,
        title: Optional[str] = None,
        profile: Optional[str] = None,
        mission: Optional[str] = None,
        organization: Optional[str] = None,
        verse: Optional[Verse] = None,
        category: Optional[Category] = None,
        contract_type: Optional[ContractType] = None,
        offer_url: Optional[HttpUrl] = None,
        publication_date: Optional[datetime] = None,
        beginning_date: Optional[LimitDate] = None,
        localisation: Optional[Localisation] = None,
        country: Optional[str] = None,
        region: Optional[str] = None,
        department: Optional[str] = None,
        updated_at: Optional[datetime] = None,
        processing: bool = False,
        processed_at: Optional[datetime] = None,
        archived_at: Optional[datetime] = None,
        save_in_db: Optional[bool] = True,
    ) -> OfferModel:
        if external_id is None:
            external_id = (
                f"test_offer_{timezone.make_aware(datetime.now()).timestamp()}"
            )

        if publication_date is None:
            publication_date = timezone.make_aware(datetime.now())

        if processed_at:
            processed_at = timezone.make_aware(processed_at)

        if archived_at:
            archived_at = timezone.make_aware(archived_at)

        if localisation is None and country and region and department:
            localisation = Localisation(
                country=Country(country),
                region=Region(code=region),
                department=Department(code=department),
            )

        offer = Offer(
            id=uuid4(),
            external_id=external_id,
            verse=verse,
            title=title or "Test Offer Title",
            profile=profile or "Test profile description",
            mission=mission or "Test mission description",
            category=category,
            contract_type=contract_type,
            organization=organization or "Test Organization",
            offer_url=offer_url,
            localisation=localisation,
            publication_date=publication_date,
            beginning_date=beginning_date,
            processing=processing,
            processed_at=processed_at,
            archived_at=archived_at,
        )

        offer_model = OfferModel.from_entity(offer)

        if save_in_db:
            offer_model.save()

            if updated_at:
                OfferModel.objects.filter(id=offer.id).update(
                    updated_at=timezone.make_aware(updated_at)
                )
                offer_model.refresh_from_db()

        return offer_model

    @staticmethod
    def create_batch(
        size: int,
        **kwargs,
    ) -> List[OfferModel]:
        return [OfferFactory.create(**kwargs) for _ in range(size)]
