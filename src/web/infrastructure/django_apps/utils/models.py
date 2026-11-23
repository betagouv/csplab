from django.db import models


class BaseDatedModel(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def related_model(model: type[models.Model], name: str) -> type[models.Model]:
    return model._meta.get_field(name).related_model  # type: ignore[return-value]
