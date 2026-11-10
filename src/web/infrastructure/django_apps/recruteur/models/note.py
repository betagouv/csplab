from typing import TYPE_CHECKING

from django.db import models

from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.users.fields import agent_fk
from infrastructure.django_apps.utils.models import BaseDatedModel

if TYPE_CHECKING:
    from infrastructure.django_apps.tag.models import TagModel


class NoteQuerySet(models.QuerySet):
    def active(self) -> "NoteQuerySet":
        return self.filter(supprimee_le__isnull=True)

    def for_team(self) -> "NoteQuerySet":
        return self.active().filter(est_privee=False)

    def personal(self) -> "NoteQuerySet":
        return self.active().filter(est_privee=True)

    def by_candidature(self, candidature_id) -> "NoteQuerySet":
        return (
            self.select_related("publie_par__utilisateur")
            .active()
            .filter(candidature_id=candidature_id)
            .order_by("-created_at")
        )

    def visibles_par(self, agent_id) -> "NoteQuerySet":
        return self.filter(
            models.Q(est_privee=False) | models.Q(publie_par_id=agent_id)
        )

    def by_candidature_and_author(self, candidature_id, agent_id) -> "NoteQuerySet":
        return self.by_candidature(candidature_id).filter(publie_par_id=agent_id)

    def by_candidature_author_and_id(
        self, candidature_id, agent_id, note_id
    ) -> "NoteQuerySet":
        return self.by_candidature_and_author(candidature_id, agent_id).filter(
            pk=note_id
        )

    def with_tags(self) -> "NoteQuerySet":
        liaison_model = self.model._meta.get_field("tags_liaisons").related_model
        return self.prefetch_related(
            models.Prefetch(
                "tags_liaisons",
                queryset=liaison_model.objects.select_related("tag").order_by(
                    "created_at", "id"
                ),
            )
        )


class NoteModel(BaseDatedModel):
    candidature = models.ForeignKey(
        CandidatureModel,
        on_delete=models.PROTECT,
        db_column="candidature_id",
        related_name="notes",
    )
    message = models.TextField()
    publie_par = agent_fk(related_name="notes_publiees")
    supprimee_le = models.DateTimeField(null=True, blank=True)
    est_privee = models.BooleanField(default=False)

    objects = NoteQuerySet.as_manager()

    class Meta:
        db_table = "note"
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self) -> str:
        return str(self.id)

    @property
    def tags(self) -> list["TagModel"]:
        return [liaison.tag for liaison in self.tags_liaisons.all()]
