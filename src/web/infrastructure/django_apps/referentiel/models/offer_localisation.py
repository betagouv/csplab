from uuid import UUID, uuid4

from django.db import models
from django.db.models import Q
from referentiel.value_objects.localisation import Localisation

from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.utils.models import BaseDatedModel


class OfferLocalisationModel(BaseDatedModel):
    offer = models.ForeignKey(
        OfferModel, on_delete=models.CASCADE, related_name="localisations"
    )
    # 0 is the main localisation
    position = models.PositiveSmallIntegerField()
    area = models.CharField(max_length=2)
    country = models.CharField(max_length=3)
    region = models.CharField(max_length=3, null=True, blank=True)
    department = models.CharField(max_length=3, null=True, blank=True)
    label = models.CharField(max_length=500, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "offer_localisations"
        verbose_name = "Offer localisation"
        verbose_name_plural = "Offer localisations"
        ordering = ["offer_id", "position"]
        constraints = [
            models.UniqueConstraint(
                fields=["offer", "position"],
                name="offer_localisations_offer_position_unique",
            ),
            models.UniqueConstraint(
                fields=["offer", "country", "region", "department", "label"],
                name="offer_localisations_no_duplicate",
                # Offers abroad have no region nor department
                nulls_distinct=False,
            ),
            models.CheckConstraint(
                condition=Q(latitude__isnull=True)
                | Q(latitude__gte=-90, latitude__lte=90),
                name="offer_localisations_latitude_range",
            ),
            models.CheckConstraint(
                condition=Q(longitude__isnull=True)
                | Q(longitude__gte=-180, longitude__lte=180),
                name="offer_localisations_longitude_range",
            ),
        ]
        indexes = [
            models.Index(fields=["department"], name="offer_loc_department_idx"),
            models.Index(fields=["region"], name="offer_loc_region_idx"),
            models.Index(fields=["country"], name="offer_loc_country_idx"),
            models.Index(fields=["area"], name="offer_loc_area_idx"),
        ]

    @classmethod
    def from_localisation(
        cls, offer_id: UUID, position: int, localisation: Localisation
    ) -> "OfferLocalisationModel":
        return cls(
            id=uuid4(),
            offer_id=offer_id,
            position=position,
            area=localisation.area.value,
            country=str(localisation.country),
            region=localisation.region.code if localisation.region else None,
            department=localisation.department.code
            if localisation.department
            else None,
            label=localisation.label or "",
            latitude=localisation.latitude,
            longitude=localisation.longitude,
        )

    def __str__(self) -> str:
        return f"{self.offer_id} #{self.position} - {self.country} {self.department}"
