from uuid import uuid4

from django.db import models
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.utils.models import BaseDatedModel


class OrganismeModel(BaseDatedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    # ── identite BC ──────────────────────────────────────────────────────
    nom = models.CharField(max_length=255)
    versant = models.CharField(
        max_length=10,
        choices=[(v.value, v.value) for v in Verse],
    )
    siret = models.CharField(max_length=14, null=True, blank=True, unique=True)
    parent_id = models.UUIDField(null=True, blank=True)
    localisation = models.JSONField(null=True, blank=True)
    # ── recruteur BC ─────────────────────────────────────────────────────
    # Ordered JSON array of recruitment steps. Each item:
    # {"entity_id": "<uuid>", "categorie": "<CategorieEtapeRecrutement.value>",
    # "nom": "<str>"}
    # The order of the array defines the order of the steps.
    etapes = models.JSONField(
        null=True,
        blank=True,
        help_text=(
            "Ordered recruitment steps. "
            "Each item: {'entity_id': str, 'categorie': str, 'nom': str}"
        ),
    )

    class Meta:
        db_table = "organisme"
        verbose_name = "Organisme"
        verbose_name_plural = "Organismes"

    def __str__(self) -> str:
        return str(self.id)
