from typing import TYPE_CHECKING, ClassVar, Self

from django.db import models

if TYPE_CHECKING:
    from infrastructure.django_apps.tag.models import TagModel


class TaggedQuerySet(models.QuerySet):
    def with_tags(self) -> Self:
        related_name = self.model.tags_related_name
        liaison_model = self.model._meta.get_field(related_name).related_model
        return self.prefetch_related(
            models.Prefetch(
                related_name,
                queryset=liaison_model.objects.select_related("tag").order_by(
                    "created_at", "id"
                ),
            )
        )


class TaggedModelMixin:
    tags_related_name: ClassVar[str] = "tags_liaisons"

    @property
    def tags(self) -> list["TagModel"]:
        liaisons = getattr(self, self.tags_related_name)
        return [liaison.tag for liaison in liaisons.all()]
