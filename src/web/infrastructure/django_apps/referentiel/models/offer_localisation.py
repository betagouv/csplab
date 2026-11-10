from collections.abc import Iterable
from uuid import UUID, uuid4

from django.db import models
from django.db.models import F, FloatField, Q, Value
from django.db.models.functions import ACos, Cos, Greatest, Least, Radians, Sin
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region

from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.utils.models import BaseDatedModel

EARTH_RADIUS_KM = 6371.0


class OfferLocalisationQuerySet(models.QuerySet):
    def located_in(
        self,
        *,
        regions: Iterable[str],
        departments: Iterable[str],
        countries: Iterable[str],
        areas: Iterable[str],
    ) -> "OfferLocalisationQuerySet | None":
        lookups = {
            f"{field}__in": list(values)
            for field, values in (
                ("region", regions),
                ("department", departments),
                ("country", countries),
                ("area", areas),
            )
            if values
        }
        return self.filter(**lookups) if lookups else None

    def within(
        self, latitude: float, longitude: float, radius_km: float
    ) -> "OfferLocalisationQuerySet":
        def radians(value: float) -> Radians:
            return Radians(Value(value, output_field=FloatField()))

        cosine = Cos(radians(latitude)) * Cos(Radians(F("latitude"))) * Cos(
            Radians(F("longitude")) - radians(longitude)
        ) + Sin(radians(latitude)) * Sin(Radians(F("latitude")))
        clamped = Least(
            Value(1.0, output_field=FloatField()),
            Greatest(Value(-1.0, output_field=FloatField()), cosine),
        )
        return (
            self.filter(latitude__isnull=False, longitude__isnull=False)
            .annotate(distance_km=EARTH_RADIUS_KM * ACos(clamped))
            .filter(distance_km__lte=radius_km)
        )


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

    objects = OfferLocalisationQuerySet.as_manager()

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

    def to_localisation(self) -> Localisation:
        return Localisation(
            area=GeographicalArea(self.area),
            country=Country(self.country),
            region=Region(code=self.region) if self.region else None,
            department=Department(code=self.department) if self.department else None,
            label=self.label or None,
            latitude=self.latitude,
            longitude=self.longitude,
        )

    def __str__(self) -> str:
        return f"{self.offer_id} #{self.position} - {self.country} {self.department}"
