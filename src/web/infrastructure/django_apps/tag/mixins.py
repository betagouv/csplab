from typing import TYPE_CHECKING, ClassVar, Self

from django.db import models

from infrastructure.django_apps.utils.models import related_model

if TYPE_CHECKING:
    from infrastructure.django_apps.tag.models import TagModel


class TaggedQuerySet(models.QuerySet):
    def with_tags(self) -> Self:
        related_name = self.model.tags_related_name
        liaison_model = related_model(self.model, related_name)
        return self.prefetch_related(
            models.Prefetch(
                related_name,
                queryset=liaison_model._default_manager.select_related("tag").order_by(
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
