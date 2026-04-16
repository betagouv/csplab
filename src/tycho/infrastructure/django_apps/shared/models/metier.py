from django.db import models

from domain.value_objects.verse import Verse


class ReferencielMetier(models.TextChoices):
    RMFP_V1 = "RMFP_V1", "Référentiel des métiers de la fonction publique - version 1"


class MetierModel(models.Model):
    objects: models.Manager = models.Manager()

    VERSE_CHOICES = [(v.value, v.name) for v in Verse]
    REFERENCIEL_METIER = [(v.value, v.name) for v in ReferencielMetier]

    id = models.UUIDField(primary_key=True)

    external_id = models.CharField(max_length=50, unique=True)
    code_emploi_csp = models.CharField(max_length=50, null=True, blank=True)

    libelle_emploi_csp = models.CharField(max_length=200, null=True, blank=True)
    referenciel_metier_id = models.CharField(
        max_length=20, choices=REFERENCIEL_METIER, null=True, blank=True
    )
    libelle_court = models.CharField(max_length=200)
    libelle_long = models.CharField(max_length=500)
    definition_synthetique = models.TextField(null=True, blank=True)

    code_domaine_fonctionnel = models.CharField(max_length=20)
    libelle_domaine_fonctionnel = models.CharField(max_length=200)
    code_famille = models.CharField(max_length=20)
    libelle_famille = models.CharField(max_length=200)

    versants = models.CharField(
        max_length=20, choices=VERSE_CHOICES, null=True, blank=True
    )

    conditions_particulieres = models.TextField(null=True, blank=True)
    competences_specifiques_fpe = models.TextField(null=True, blank=True)
    competences_specifiques_fpt = models.TextField(null=True, blank=True)
    competences_specifiques_fph = models.TextField(null=True, blank=True)

    activites = models.JSONField(default=list)
    competences = models.JSONField(default=list)

    processing = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "metiers"
        verbose_name = "Métier"
        verbose_name_plural = "Métiers"
        indexes = [
            models.Index(fields=["external_id"]),
            models.Index(fields=["code_emploi_csp"]),
        ]

    def __str__(self) -> str:
        return f"{self.external_id} - {self.libelle_court}"
