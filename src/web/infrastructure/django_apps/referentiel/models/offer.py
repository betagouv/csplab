from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.ingestion.models.source import SourceModel
from infrastructure.django_apps.utils.models import BaseDatedModel


class OfferModel(BaseDatedModel):
    # Contract type choices from ContractType enum
    CONTRACT_TYPE_CHOICES = [(ct.value, ct.name) for ct in ContractType]

    # Category choices from Category enum
    CATEGORY_CHOICES = [(cat.value, cat.name) for cat in Category]

    # Verse choices from Verse enum
    VERSE_CHOICES = [(v.value, v.name) for v in Verse]

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
    location_label = models.CharField(max_length=500, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    long_title = models.CharField(max_length=1500, null=True, blank=True)
    application_url = models.URLField(null=True, blank=True)
    contract_kind = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)
    job_vacancy = models.CharField(max_length=50, null=True, blank=True)
    employer = models.TextField(null=True, blank=True)
    complements = models.TextField(null=True, blank=True)
    criteria = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)
    conditions = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)
    contacts = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)

    # Date fields
    publication_date = models.DateTimeField()
    beginning_date = models.DateTimeField(null=True, blank=True)
    processing = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)

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

    def __str__(self) -> str:
        return f"Offer {self.external_id} - {self.title}"
