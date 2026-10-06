from django.db import connection, models, transaction

from infrastructure.django_apps.referentiel.models.offer import OfferModel


def format_reference(year: int, number: int) -> str:
    return f"CSP-{year}-{number:06d}"


class OfferReferenceSequenceManager(models.Manager["OfferReferenceSequenceModel"]):
    def next_references(self, year: int, count: int) -> list[str]:
        references: list[str] = []
        with transaction.atomic():
            while len(references) < count:
                candidates = self._reserve(year, count - len(references))
                taken = set(
                    OfferModel.objects.filter(reference__in=candidates).values_list(
                        "reference", flat=True
                    )
                )
                references.extend(c for c in candidates if c not in taken)
        return references

    def _reserve(self, year: int, count: int) -> list[str]:
        table = self.model._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO {table} (year, last_value) VALUES (%s, %s)
                ON CONFLICT (year)
                DO UPDATE SET last_value = {table}.last_value + EXCLUDED.last_value
                RETURNING last_value
                """,  # noqa: S608
                [year, count],
            )
            (last_value,) = cursor.fetchone()
        return [
            format_reference(year, number)
            for number in range(last_value - count + 1, last_value + 1)
        ]


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
