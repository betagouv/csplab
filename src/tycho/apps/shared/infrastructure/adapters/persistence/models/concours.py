"""Django model for Concours entity."""

from django.contrib.postgres.fields import ArrayField
from django.db import models

from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.ministry import Ministry
from core.value_objects.nor import NOR
from domain.entities.concours import Concours


class ConcoursModel(models.Model):
    """Django model for Concours entity persistence."""

    objects: models.Manager = models.Manager()

    id = models.AutoField(primary_key=True)
    corps = models.CharField(max_length=200, default="")
    grade = models.CharField(max_length=200, default="", blank=True)
    nor_original = models.CharField(max_length=50)
    nor_list = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    category = models.CharField(max_length=20)
    ministry = models.CharField(max_length=100)
    access_modality = ArrayField(
        models.CharField(max_length=50), blank=True, default=list
    )
    written_exam_date = models.DateTimeField(null=True, blank=True)
    open_position_number = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta configuration for ConcoursModel."""

        db_table = "concours"
        verbose_name = "Concours"
        verbose_name_plural = "Concours"
        indexes = [
            models.Index(fields=["nor_original"]),
        ]

    def to_entity(self) -> Concours:
        """Convert Django model to Concours entity."""
        return Concours(
            id=self.id,
            corps=self.corps,
            grade=self.grade,
            nor_original=NOR(self.nor_original),
            nor_list=[NOR(nor) for nor in self.nor_list],
            category=Category(self.category),
            ministry=Ministry(self.ministry),
            access_modality=[
                AccessModality(modality) for modality in self.access_modality
            ],
            written_exam_date=self.written_exam_date,
            open_position_number=self.open_position_number,
        )

    @classmethod
    def from_entity(cls, concours: Concours) -> "ConcoursModel":
        """Create Django model from Concours entity."""
        return cls(
            id=concours.id,
            corps=concours.corps,
            grade=concours.grade,
            nor_original=concours.nor_original.value,
            nor_list=[nor.value for nor in concours.nor_list],
            category=concours.category.value,
            ministry=concours.ministry.value,
            access_modality=[modality.value for modality in concours.access_modality],
            written_exam_date=concours.written_exam_date,
            open_position_number=concours.open_position_number,
        )

    def __str__(self) -> str:
        """String representation of ConcoursModel."""
        return f"Concours {self.nor_original} - {self.ministry}"
