"""Django model for Offer entity."""

from django.db import models

from domain.entities.offer import Offer
from domain.value_objects.category import Category
from domain.value_objects.department import Department
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.region import Region
from domain.value_objects.verse import Verse


class OfferModel(models.Model):
    """Django model for Offer entity persistence."""

    objects: models.Manager = models.Manager()

    id = models.AutoField(primary_key=True)
    external_id = models.CharField(max_length=100, unique=True)
    verse = models.CharField(max_length=20)
    titre = models.CharField(max_length=500)
    profile = models.TextField()
    category = models.CharField(max_length=20)

    # Localisation fields stored separately
    region = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)

    # LimitDate as DateTimeField
    limit_date = models.DateTimeField(null=True, blank=True)

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
        if self.region and self.department:
            localisation = Localisation(
                region=Region(self.region), department=Department(self.department)
            )

        # Build limit_date if present
        limit_date = LimitDate(self.limit_date) if self.limit_date else None

        return Offer(
            id=self.id,
            external_id=self.external_id,
            verse=Verse(self.verse),
            titre=self.titre,
            profile=self.profile,
            category=Category(self.category),
            localisation=localisation,
            limit_date=limit_date,
        )

    @classmethod
    def from_entity(cls, offer: Offer) -> "OfferModel":
        """Create OfferModel instance from Offer entity."""
        # Extract localisation fields
        region = None
        department = None
        if offer.localisation:
            region = offer.localisation.region.value
            department = offer.localisation.department.value

        # Extract limit_date
        limit_date = None
        if offer.limit_date:
            limit_date = offer.limit_date.value

        return cls(
            id=offer.id,
            external_id=offer.external_id,
            verse=offer.verse.value,
            titre=offer.titre,
            profile=offer.profile,
            category=offer.category.value,
            region=region,
            department=department,
            limit_date=limit_date,
        )

    def __str__(self) -> str:
        """String representation of OfferModel."""
        return f"Offer {self.external_id} - {self.titre}"
