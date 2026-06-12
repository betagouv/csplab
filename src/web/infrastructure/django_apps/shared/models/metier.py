from django.db import models
from referentiel.entities.metier import Metier
from referentiel.value_objects.verse import Verse


class MetierModel(models.Model):
    id = models.UUIDField(primary_key=True)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "metiers"
        verbose_name = "Métier"
        verbose_name_plural = "Métiers"
        indexes = [
            models.Index(fields=["external_id"]),
        ]

    def to_entity(self):
        versants = (
            [Verse(verse) for verse in self.versants if verse] if self.versants else []
        )

        return Metier(
            id=self.id,
            external_id=self.external_id,
            libelle=self.libelle_long,
            description=self.definition_synthetique or "",
            domaine_fonctionnel_code=self.domaine_fonctionnel_code,
            versants=versants,
            activites=self.activites or [],
            conditions_particulieres=self.conditions_particulieres or [],
            offer_family_code=self.offer_family_code,
        )

    @classmethod
    def from_entity(cls, metier):

        versants = (
            [verse.value for verse in metier.versants] if metier.versants else None
        )

        return cls(
            id=metier.id,
            external_id=metier.external_id,
            libelle_long=metier.libelle,
            definition_synthetique=metier.description,
            domaine_fonctionnel_code=metier.domaine_fonctionnel_code,
            offer_family_code=metier.offer_family_code or "",
            versants=versants,
            activites=metier.activites,
            conditions_particulieres=metier.conditions_particulieres,
        )
