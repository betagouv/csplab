"""Django model for Offer entity."""

from django.db import models
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


class OfferModel(models.Model):
    """Django model for Offer entity persistence."""

    objects: models.Manager = models.Manager()

    # Contract type choices from ContractType enum
    CONTRACT_TYPE_CHOICES = [(ct.value, ct.name) for ct in ContractType]

    # Category choices from Category enum
    CATEGORY_CHOICES = [(cat.value, cat.name) for cat in Category]

    # Verse choices from Verse enum
    VERSE_CHOICES = [(v.value, v.name) for v in Verse]

    id = models.UUIDField(primary_key=True)
    external_id = models.CharField(max_length=100, unique=True)
    verse = models.CharField(
        max_length=20, choices=VERSE_CHOICES, null=True, blank=True
    )
    title = models.CharField(max_length=500)
    profile = models.TextField()
    mission = models.TextField()
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True
    )
    contract_type = models.CharField(
        max_length=25, choices=CONTRACT_TYPE_CHOICES, null=True, blank=True
    )
    organization = models.CharField(max_length=500)
    offer_url = models.URLField(null=True, blank=True)

    # Localisation fields stored separately
    country = models.CharField(max_length=3, null=True, blank=True)
    region = models.CharField(max_length=3, null=True, blank=True)
    department = models.CharField(max_length=3, null=True, blank=True)

    # Date fields
    publication_date = models.DateTimeField()
    beginning_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta configuration for OfferModel."""

        db_table = "offers"
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
        indexes = [
            models.Index(fields=["external_id"]),
        ]

    def to_entity(self) -> Offer:
        """Convert OfferModel instance to Offer entity."""
        # Build localisation if both region and department are present
        localisation = None
        if self.region and self.department and self.country:
            localisation = Localisation(
                country=Country(self.country),
                region=Region(code=self.region),
                department=Department(code=self.department),
            )

        beginning_date = LimitDate(self.beginning_date) if self.beginning_date else None

        category = Category(self.category) if self.category else None

        contract_type = ContractType(self.contract_type) if self.contract_type else None

        offer_url = HttpUrl(self.offer_url) if self.offer_url else None

        verse = Verse(self.verse) if self.verse else None

        return Offer(
            id=self.id,
            external_id=self.external_id,
            verse=verse,
            title=self.title,
            profile=self.profile,
            mission=self.mission,
            category=category,
            contract_type=contract_type,
            organization=self.organization,
            offer_url=offer_url,
            localisation=localisation,
            publication_date=self.publication_date,
            beginning_date=beginning_date,
        )

    @classmethod
    def from_entity(cls, offer: Offer) -> "OfferModel":
        """Create OfferModel instance from Offer entity."""
        # Extract localisation fields
        country = None
        region = None
        department = None
        if offer.localisation:
            country = str(offer.localisation.country)  # Use ISO-3 code (e.g., "FRA")
            region = offer.localisation.region.code
            department = offer.localisation.department.code

        # Extract beginning_date
        beginning_date = None
        if offer.beginning_date:
            beginning_date = offer.beginning_date.value

        # Extract category
        category = offer.category.value if offer.category else None

        # Extract contract_type
        contract_type = offer.contract_type.value if offer.contract_type else None

        # Extract offer_url
        offer_url = str(offer.offer_url) if offer.offer_url else None

        return cls(
            id=offer.id,
            external_id=offer.external_id,
            verse=offer.verse.value if offer.verse else None,
            title=offer.title,
            profile=offer.profile,
            mission=offer.mission,
            category=category,
            contract_type=contract_type,
            organization=offer.organization,
            offer_url=offer_url,
            country=country,
            region=region,
            department=department,
            publication_date=offer.publication_date,
            beginning_date=beginning_date,
        )

    def __str__(self) -> str:
        """String representation of OfferModel."""
        return f"Offer {self.external_id} - {self.title}"
