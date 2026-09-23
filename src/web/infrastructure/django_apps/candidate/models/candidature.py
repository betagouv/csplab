from django.db import models

from domain.candidate.value_objects.statut_candidature import StatutCandidature
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.users.fields import candidat_fk
from infrastructure.django_apps.utils.models import BaseDatedModel


class CandidatureQuerySet(models.QuerySet):
    def by_recrutement_and_candidature(
        self, recrutement_id, candidature_id
    ) -> "CandidatureQuerySet":
        return self.filter(etape__recrutement_id=recrutement_id, pk=candidature_id)

    def by_etape(self, etape_id) -> "CandidatureQuerySet":
        return self.filter(etape_id=etape_id).order_by("created_at")

    def with_detail(self) -> "CandidatureQuerySet":
        return self.select_related(
            "candidat__utilisateur", "etape__recrutement__offre"
        ).prefetch_related("etape__recrutement__etapes")


class CandidatureModel(BaseDatedModel):
    candidat = candidat_fk(related_name="candidatures")
    statut = models.CharField(
        max_length=20,
        choices=[(s.value, s.value) for s in StatutCandidature],
        default=StatutCandidature.INITIAL.value,
    )
    updated_by_candidate = models.DateTimeField(null=True, blank=True)
    updated_by_recruteur = models.DateTimeField(null=True, blank=True)
    documents = models.JSONField(null=True, blank=True)
    motif_refus = models.CharField(
        max_length=50,
        choices=MotifRefus.choices,
        null=True,
        blank=True,
    )
    etape = models.ForeignKey(
        EtapeModel,
        on_delete=models.PROTECT,
        db_column="etape_id",
        related_name="candidatures",
        help_text=(
            "Étape courante du recrutement (par défaut, l'étape ENTREE "
            "du recrutement correspondant à l'offre)."
        ),
    )

    objects = CandidatureQuerySet.as_manager()

    class Meta:
        db_table = "candidature"
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"
        constraints = [
            models.UniqueConstraint(
                fields=["candidat_id", "etape_id"],
                name="unique_candidature_candidat_etape",
            )
        ]

    def __str__(self) -> str:
        return str(self.id)
