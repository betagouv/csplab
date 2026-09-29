from uuid import uuid4

from django.db import models
from referentiel.entities.talentsoft_organisme import TalentsoftOrganisme

from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.utils.models import BaseDatedModel


class TalentsoftOrganismeQuerySet(models.QuerySet):
    def by_organisme_ids(self, organisme_ids: list) -> "TalentsoftOrganismeQuerySet":
        return self.filter(organisme_id__in=organisme_ids)

    def by_entity_codes(self, entity_codes: list) -> "TalentsoftOrganismeQuerySet":
        return self.filter(entity_code__in=entity_codes)

    def by_entity_code(self, entity_code: str) -> "TalentsoftOrganismeQuerySet":
        return self.filter(entity_code=entity_code)


class TalentsoftOrganismeModel(BaseDatedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    entity_code = models.CharField(max_length=50, unique=True)
    code = models.IntegerField(unique=True)
    organisme = models.ForeignKey(
        OrganismeModel,
        on_delete=models.SET_NULL,
        db_column="organisme_id",
        related_name="talentsoft_organismes",
        null=True,
        blank=True,
    )
    parent_code = models.IntegerField(null=True, blank=True)
    has_children = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    post_code = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    parent_name = models.CharField(max_length=255, null=True, blank=True)
    logo_url = models.URLField(max_length=500, null=True, blank=True)
    max_delay_for_consent = models.IntegerField(null=True, blank=True)
    retention_period = models.IntegerField(null=True, blank=True)
    general_conditions = models.TextField(null=True, blank=True)
    personal_data_consent = models.TextField(null=True, blank=True)

    objects = TalentsoftOrganismeQuerySet.as_manager()

    class Meta:
        db_table = "talentsoft_organisme"
        verbose_name = "Organisme Talentsoft"
        verbose_name_plural = "Organismes Talentsoft"

    def __str__(self) -> str:
        return f"{self.entity_code} - {self.name}"

    def to_entity(self) -> TalentsoftOrganisme:
        return TalentsoftOrganisme(
            entity_code=self.entity_code,
            code=self.code,
            name=self.name,
            parent_code=self.parent_code,
            has_children=self.has_children,
            description=self.description,
            url=self.url,
            phone_number=self.phone_number,
            post_code=self.post_code,
            latitude=self.latitude,
            longitude=self.longitude,
            parent_name=self.parent_name,
            logo_url=self.logo_url,
            max_delay_for_consent=self.max_delay_for_consent,
            retention_period=self.retention_period,
            general_conditions=self.general_conditions,
            personal_data_consent=self.personal_data_consent,
        )
