"""Django model for Corps entity."""

from django.db import models

from domain.entities.corps import Corps
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.diploma import Diploma
from domain.value_objects.label import Label
from domain.value_objects.ministry import Ministry


class CorpsModel(models.Model):
    """Django model for Corps entity persistence."""

    objects: models.Manager = models.Manager()

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50)
    category = models.CharField(max_length=20, null=True, blank=True)
    ministry = models.CharField(max_length=100)
    diploma_level = models.IntegerField(null=True, blank=True)
    short_label = models.CharField(max_length=200)
    long_label = models.TextField()
    access_modalities = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta configuration for CorpsModel."""

        db_table = "corps"
        verbose_name = "Corps"
        verbose_name_plural = "Corps"

    def to_entity(self) -> Corps:
        """Convert Django model to Corps entity."""
        category = Category(self.category) if self.category else None

        ministry = Ministry(self.ministry)

        diploma = Diploma(value=self.diploma_level) if self.diploma_level else None

        label = Label(short_value=self.short_label, value=self.long_label)

        access_modalities = [
            AccessModality(modality) for modality in self.access_modalities
        ]

        return Corps(
            id=self.id,
            code=self.code,
            category=category,
            ministry=ministry,
            diploma=diploma,
            access_modalities=access_modalities,
            label=label,
        )

    @classmethod
    def from_entity(cls, corps: Corps) -> "CorpsModel":
        """Create Django model from Corps entity."""
        return cls(
            id=corps.id,
            code=corps.code,
            category=corps.category.value if corps.category else None,
            ministry=corps.ministry.value,
            diploma_level=corps.diploma.value if corps.diploma else None,
            short_label=corps.label.short_value,
            long_label=corps.label.value,
            access_modalities=[modality.value for modality in corps.access_modalities],
        )

    def __str__(self) -> str:
        """String representation of CorpsModel."""
        return f"{self.code} - {self.short_label}"
