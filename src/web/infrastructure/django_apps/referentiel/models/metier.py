from django.db import models

from infrastructure.django_apps.utils.models import BaseDatedModel


class MetierQuerySet(models.QuerySet):
    def by_offer_family_code(self, offer_family_code: str) -> "MetierQuerySet":
        return self.filter(offer_family_code=offer_family_code)

    def active(self) -> "MetierQuerySet":
        return self.filter(archived_at__isnull=True)

    def functional_area_codes(self) -> set[str]:
        return set(self.values_list("domaine_fonctionnel_code", flat=True))


class MetierModel(BaseDatedModel):
    external_id = models.CharField(max_length=8, unique=True)
    libelle_long = models.CharField(max_length=500)
    definition_synthetique = models.TextField(null=True, blank=True)
    domaine_fonctionnel_code = models.CharField(max_length=3)
    offer_family_code = models.CharField(max_length=8)
    versants = models.JSONField(default=list, null=True, blank=True)
    conditions_particulieres = models.JSONField(default=list, null=True, blank=True)
    activites = models.JSONField(default=list)

    processing = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    objects = MetierQuerySet.as_manager()

    class Meta:
        db_table = "metiers"
        verbose_name = "Métier"
        verbose_name_plural = "Métiers"
        indexes = [
            models.Index(fields=["external_id"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(offer_family_code=""),
                name="metiers_offer_family_code_not_empty",
            ),
        ]
