from datetime import UTC, datetime
from uuid import uuid4

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)


class OfferDjangoFactory(DjangoModelFactory):
    class Meta:
        model = OfferModel
        skip_postgeneration_save = True

    id = factory.LazyFunction(uuid4)
    source = factory.SubFactory(SourceDjangoFactory)
    external_id = factory.Sequence(lambda n: f"OFFER_{n}")
    reference = factory.LazyFunction(lambda: str(uuid4()))
    verse = Verse.FPE.value
    title = "Test Offer Title"
    profile = "Test profile description"
    mission = "Test mission description"
    category = Category.A.value
    organization = "Test Organization"
    publication_date = datetime(2024, 1, 15, tzinfo=UTC)
    beginning_date = datetime(2024, 12, 31, tzinfo=UTC)
    area = GeographicalArea.EUROPE.value
    country = "FRA"
    region = "11"
    department = "75"
    processing = False
    processed_at = None
    archived_at = None

    @factory.post_generation
    def updated_at(self, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        OfferModel.objects.filter(id=self.id).update(
            updated_at=timezone.make_aware(extracted)
        )
        self.refresh_from_db()
