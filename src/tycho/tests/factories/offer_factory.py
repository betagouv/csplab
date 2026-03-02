from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from django.utils import timezone

from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
from domain.value_objects.verse import Verse
from infrastructure.django_apps.shared.models.offer import OfferModel


class OfferFactory:
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
        offer_url: Optional[str] = None,
        publication_date: Optional[datetime] = None,
        beginning_date: Optional[datetime] = None,
        country: Optional[str] = None,
        region: Optional[str] = None,
        department: Optional[str] = None,
        updated_at: Optional[datetime] = None,
        processing: bool = False,
        processed_at: Optional[datetime] = None,
        archived_at: Optional[datetime] = None,
    ) -> OfferModel:
        if external_id is None:
            external_id = (
                f"test_offer_{timezone.make_aware(datetime.now()).timestamp()}"
            )

        if title is None:
            title = "Test Offer Title"

        if profile is None:
            profile = "Test profile description"

        if mission is None:
            mission = "Test mission description"

        if organization is None:
            organization = "Test Organization"

        if publication_date is None:
            publication_date = timezone.make_aware(datetime.now())

        if processed_at:
            processed_at = timezone.make_aware(processed_at)

        if archived_at:
            archived_at = timezone.make_aware(archived_at)

        offer = OfferModel(
            id=uuid4(),
            external_id=external_id,
            verse=verse.value if verse else None,
            title=title,
            profile=profile,
            mission=mission,
            category=category.value if category else None,
            contract_type=contract_type.value if contract_type else None,
            organization=organization,
            offer_url=offer_url,
            country=country,
            region=region,
            department=department,
            publication_date=publication_date,
            beginning_date=beginning_date,
            processing=processing,
            processed_at=processed_at,
            archived_at=archived_at,
        )

        offer.save()

        if updated_at:
            OfferModel.objects.filter(id=offer.id).update(
                updated_at=timezone.make_aware(updated_at)
            )
            offer.refresh_from_db()

        return offer

    @staticmethod
    def create_batch(
        size: int,
        **kwargs,
    ) -> List[OfferModel]:
        return [OfferFactory.create(**kwargs) for _ in range(size)]
