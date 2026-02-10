"""Factory for generating test Offer instances."""

from datetime import datetime, timezone
from typing import Optional

from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
from domain.value_objects.verse import Verse
from infrastructure.django_apps.shared.models.offer import OfferModel


class OfferFactory:
    """Factory for creating Offer test instances."""

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
    ) -> OfferModel:
        """Create an OfferModel instance."""
        if external_id is None:
            external_id = f"test_offer_{datetime.now(timezone.utc).timestamp()}"

        if title is None:
            title = "Test Offer Title"

        if profile is None:
            profile = "Test profile description"

        if mission is None:
            mission = "Test mission description"

        if organization is None:
            organization = "Test Organization"

        if publication_date is None:
            publication_date = datetime.now(timezone.utc)

        offer = OfferModel(
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
        )

        offer.save()

        return offer
