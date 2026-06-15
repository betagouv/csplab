from django.db import models
from pydantic import HttpUrl
from referentiel.entities.offer import Offer
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.ingestion.models.source import SourceModel


class OfferModel(models.Model):
    # Contract type choices from ContractType enum
    CONTRACT_TYPE_CHOICES = [(ct.value, ct.name) for ct in ContractType]

    # Category choices from Category enum
    CATEGORY_CHOICES = [(cat.value, cat.name) for cat in Category]

    # Verse choices from Verse enum
    VERSE_CHOICES = [(v.value, v.name) for v in Verse]

    id = models.UUIDField(primary_key=True)
    external_id = models.CharField(max_length=100, unique=True)
    reference = models.CharField(max_length=100, null=False, blank=False)
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
    code_emploi_csp = models.CharField(max_length=50, null=True, blank=True)
    source = models.ForeignKey(
        SourceModel,
        to_field="source_id",
        on_delete=models.PROTECT,
        related_name="offers",
    )

    # Localisation fields stored separately
    area = models.CharField(max_length=2, null=True, blank=True)
    country = models.CharField(max_length=3, null=True, blank=True)
    region = models.CharField(max_length=3, null=True, blank=True)
    department = models.CharField(max_length=3, null=True, blank=True)

    # Date fields
    publication_date = models.DateTimeField()
    beginning_date = models.DateTimeField(null=True, blank=True)
    processing = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "offers"
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
        indexes = [
            models.Index(fields=["external_id"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["reference", "source_id"],
                name="offers_reference_source_id_unique",
            ),
        ]

    def to_entity(self) -> Offer:
        # Build localisation if both region and department are present
        localisation = None

        if self.region and self.department and self.country and self.area:
            localisation = Localisation(
                area=GeographicalArea(self.area),
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
            reference=self.reference,
            processing=self.processing,
            processed_at=self.processed_at,
            archived_at=self.archived_at,
            family_code=self.code_emploi_csp,
            source_id=self.source_id,
        )

    @classmethod
    def from_entity(cls, offer: Offer) -> "OfferModel":
        # Extract localisation fields
        area = None
        country = None
        region = None
        department = None
        if offer.localisation:
            area = offer.localisation.area.value
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
            reference=offer.reference,
            verse=offer.verse.value if offer.verse else None,
            title=offer.title,
            profile=offer.profile,
            mission=offer.mission,
            category=category,
            contract_type=contract_type,
            organization=offer.organization,
            offer_url=offer_url,
            area=area,
            country=country,
            region=region,
            department=department,
            code_emploi_csp=offer.family_code,
            source_id=offer.source_id,
            publication_date=offer.publication_date,
            beginning_date=beginning_date,
            processing=offer.processing,
            processed_at=offer.processed_at,
            archived_at=offer.archived_at,
        )

    def __str__(self) -> str:
        return f"Offer {self.external_id} - {self.title}"
