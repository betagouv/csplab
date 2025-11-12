from django.db import models

class LawNature(models.TextChoices):
    DECREE = 'DECREE' #translation in FR: "Decret"
    ORDER = 'ORDER' #translation in FR: "Arrêté"
    LAW = 'LAW' #translation in FR: "Loi"

class LawState(models.TextChoices):
    EFFECTIVE = 'EFFECTIVE' #translation in FR: "Vigueur"
    REPEALED = 'REPEALED' #translation in FR: "Abrogé"

class RawExamination(models.Model):
    nor = models.CharField("Code NOR", max_length=20, null=True, blank=True, unique=True, db_index=True)
    legitext_id = models.CharField("LEGITEXT ID", max_length=20, null=True, blank=True, unique=True, db_index=True)
    law_id = models.CharField("Numéro de Décret ou Arrêté ou Code", max_length=50, null=True, blank=True, unique=True, db_index=True)

    # Métadonnées
    nature = models.CharField("Nature de la Loi", max_length=10, choices=LawNature.choices, null=True, blank=True)
    title = models.CharField("Titre du texte", max_length=500, null=True, blank=True)
    publication_date = models.DateTimeField("Date de publication", null=True, blank=True)
    state = models.CharField("Etat du texte", max_length=10, choices=LawState.choices, null=True, blank=True)

    # Contenu brut
    raw_content = models.JSONField("Contenu brut du texte", null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "RawExamination"
        verbose_name_plural = "RawExaminations"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.law_id} - {self.title[:50]}"
