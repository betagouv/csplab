from django.db import models
from django.db.models import Case, Count, OuterRef, Subquery, Value, When
from django.db.models.functions import Coalesce, Lower, Trim

from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
)
from infrastructure.django_apps.utils.models import BaseDatedModel


class TagCategory(models.TextChoices):
    CANDIDATURE = "candidature", "Candidature"
    RECRUTEMENT_AGENT = "recrutement_agent", "Membre recrutement"
    NOTE = "note", "Note"


class TagColor(models.TextChoices):
    VERT = "vert", "Vert"
    MENTHE = "menthe", "Menthe"
    BLEU = "bleu", "Bleu"
    VIOLET = "violet", "Violet"
    ROSE = "rose", "Rose"
    ORANGE = "orange", "Orange"
    BEIGE = "beige", "Beige"
    JAUNE = "jaune", "Jaune"
    GRIS = "gris", "Gris"


class TagQuerySet(models.QuerySet):
    def by_organisme(self, organisme_id) -> "TagQuerySet":
        return self.filter(organisme_id=organisme_id)

    def by_id(self, organisme_id, tag_id) -> "TagQuerySet":
        return self.by_organisme(organisme_id).filter(pk=tag_id)

    def alphabetical(self, organisme_id) -> "TagQuerySet":
        return self.by_organisme(organisme_id).order_by(Lower("name"), "category")

    def by_category(self, organisme_id, category: TagCategory) -> "TagQuerySet":
        return self.alphabetical(organisme_id).filter(category=category)

    def with_usage_count(self) -> "TagQuerySet":
        return self.annotate(
            usage_count=Case(
                When(
                    category=TagCategory.CANDIDATURE,
                    then=_count_by_tag(CandidatureTagModel.objects.all()),
                ),
                When(
                    category=TagCategory.RECRUTEMENT_AGENT,
                    then=_count_by_tag(
                        RecrutementAgentTagModel.objects.filter(
                            recrutement_agent__date_revocation__isnull=True
                        )
                    ),
                ),
                When(
                    category=TagCategory.NOTE,
                    then=_count_by_tag(
                        NoteTagModel.objects.filter(note__supprimee_le__isnull=True)
                    ),
                ),
                default=Value(0),
                output_field=models.IntegerField(),
            )
        )


def _count_by_tag(liaisons: models.QuerySet) -> Coalesce:
    return Coalesce(
        Subquery(
            liaisons.filter(tag=OuterRef("pk"))
            .order_by()
            .values("tag")
            .annotate(count=Count("pk"))
            .values("count")
        ),
        0,
    )


class TagModel(BaseDatedModel):
    organisme = models.ForeignKey(
        OrganismeModel,
        on_delete=models.CASCADE,
        db_column="organisme_id",
        related_name="tags",
    )
    name = models.CharField(max_length=25)
    category = models.CharField(max_length=20, choices=TagCategory.choices)
    color = models.CharField(
        max_length=20, choices=TagColor.choices, default=TagColor.BLEU
    )

    objects = TagQuerySet.as_manager()

    class Meta:
        db_table = "tag"
        verbose_name = "Étiquette"
        verbose_name_plural = "Étiquettes"
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "organisme",
                "category",
                name="tag_unique_name_per_organisme_category",
            ),
            # TODO : renommer (couvre aussi les noms non trimés), lors d'une
            # prochaine migration
            models.CheckConstraint(
                condition=models.Q(name=Trim("name")) & ~models.Q(name=""),
                name="tag_name_non_vide",
            ),
        ]

    def __str__(self) -> str:
        return self.name


class CandidatureTagModel(BaseDatedModel):
    tag = models.ForeignKey(
        TagModel, on_delete=models.CASCADE, related_name="candidatures_liaisons"
    )
    candidature = models.ForeignKey(
        CandidatureModel,
        on_delete=models.CASCADE,
        db_column="candidature_id",
        related_name="tags_liaisons",
    )

    class Meta:
        db_table = "candidature_tag"
        verbose_name = "Étiquette de candidature"
        verbose_name_plural = "Étiquettes de candidature"
        constraints = [
            models.UniqueConstraint(
                fields=["tag", "candidature"], name="candidature_tag_unique"
            )
        ]

    def __str__(self) -> str:
        return f"{self.candidature_id} - {self.tag_id}"


class RecrutementAgentTagModel(BaseDatedModel):
    tag = models.ForeignKey(
        TagModel, on_delete=models.CASCADE, related_name="recrutement_agents_liaisons"
    )
    recrutement_agent = models.ForeignKey(
        RecrutementAgentModel,
        on_delete=models.CASCADE,
        db_column="recrutement_agent_id",
        related_name="tags_liaisons",
    )

    class Meta:
        db_table = "recrutement_agent_tag"
        verbose_name = "Étiquette de membre recrutement"
        verbose_name_plural = "Étiquettes de membre recrutement"
        constraints = [
            models.UniqueConstraint(
                fields=["recrutement_agent"], name="recrutement_agent_tag_unique"
            )
        ]

    def __str__(self) -> str:
        return f"{self.recrutement_agent_id} - {self.tag_id}"


class NoteTagModel(BaseDatedModel):
    tag = models.ForeignKey(
        TagModel, on_delete=models.CASCADE, related_name="notes_liaisons"
    )
    note = models.ForeignKey(
        NoteModel,
        on_delete=models.CASCADE,
        db_column="note_id",
        related_name="tags_liaisons",
    )

    class Meta:
        db_table = "note_tag"
        verbose_name = "Étiquette de note"
        verbose_name_plural = "Étiquettes de note"
        constraints = [
            models.UniqueConstraint(fields=["tag", "note"], name="note_tag_unique")
        ]

    def __str__(self) -> str:
        return f"{self.note_id} - {self.tag_id}"
