from django.db import models, transaction
from django.db.models import F


class OfferReferenceSequenceManager(models.Manager["OfferReferenceSequenceModel"]):
    def reserve(self, year: int, count: int) -> range:
        with transaction.atomic():
            self.bulk_create(
                [self.model(year=year, last_value=0)], ignore_conflicts=True
            )
            sequence = self.filter(year=year)
            sequence.update(last_value=F("last_value") + count)
            last_value = sequence.values_list("last_value", flat=True).get()
        return range(last_value - count + 1, last_value + 1)


class OfferReferenceSequenceModel(models.Model):
    year = models.PositiveSmallIntegerField(primary_key=True)
    last_value = models.PositiveIntegerField()

    objects = OfferReferenceSequenceManager()

    class Meta:
        db_table = "offer_reference_sequences"
        verbose_name = "Séquence de références d'offres"
        verbose_name_plural = "Séquences de références d'offres"

    def __str__(self) -> str:
        return f"{self.year}: {self.last_value}"
