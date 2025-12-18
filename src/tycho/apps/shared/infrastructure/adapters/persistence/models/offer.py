"""Django model for Offer entity."""

from datetime import datetime, time

from django.db import models
from django.utils import timezone

from core.entities.offer import Offer
from core.errors.offer_errors import MissingCategoryError, MissingVerseError
from core.value_objects.category import Category
from core.value_objects.department import Department
from core.value_objects.limit_date import LimitDate
from core.value_objects.localisation import Localisation
from core.value_objects.region import Region
from core.value_objects.verse import Verse


class OfferModel(models.Model):
    """Django model for Offer entity persistence."""

    objects: models.Manager = models.Manager()

    id = models.IntegerField(primary_key=True)
    external_id = models.CharField(max_length=100, unique=True)
    titre = models.CharField(max_length=500)
    profile = models.TextField()
    category = models.CharField(max_length=10, null=True, blank=True)
    verse = models.CharField(max_length=10, null=True, blank=True)

    # Localisation fields separated
    region = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)

    # Limit date as simple date field
    limit_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta configuration for OfferModel."""

        db_table = "offers"
        verbose_name = "Offer"
        verbose_name_plural = "Offers"

    def to_entity(self) -> Offer:
        """Convert Django model to Offer entity."""
        # Category and verse are required in Offer entity
        if not self.category:
            raise MissingCategoryError(self.external_id)
        if not self.verse:
            raise MissingVerseError(self.external_id)

        category = Category(self.category)
        verse = Verse(self.verse)

        localisation = None
        if self.region and self.department:
            localisation = Localisation(
                region=Region(self.region), department=Department(self.department)
            )

        limit_date = None
        if self.limit_date:
            limit_datetime = timezone.make_aware(
                datetime.combine(self.limit_date, time(23, 59, 59))
            )
            limit_date = LimitDate(limit_datetime)

        return Offer(
            id=self.id,
            external_id=self.external_id,
            titre=self.titre,
            profile=self.profile,
            category=category,
            verse=verse,
            localisation=localisation,
            limit_date=limit_date,
        )

    @classmethod
    def from_entity(cls, offer: Offer) -> "OfferModel":
        """Create Django model from Offer entity."""
        region = (
            offer.localisation.region.value
            if offer.localisation and offer.localisation.region
            else None
        )
        department = (
            offer.localisation.department.value
            if offer.localisation and offer.localisation.department
            else None
        )
        limit_date_value = None
        if offer.limit_date:
            # Convert datetime to date for Django DateField
            limit_date_value = offer.limit_date.value.date()

        return cls(
            id=offer.id,
            external_id=offer.external_id,
            titre=offer.titre,
            profile=offer.profile,
            category=offer.category.value if offer.category else None,
            verse=offer.verse.value if offer.verse else None,
            region=region,
            department=department,
            limit_date=limit_date_value,
        )

    def __str__(self) -> str:
        """String representation of OfferModel."""
        return f"{self.external_id} - {self.titre}"
