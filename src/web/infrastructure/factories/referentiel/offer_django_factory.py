from datetime import UTC, datetime
from uuid import uuid4

import factory
from factory.django import DjangoModelFactory
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.referentiel.models.offer_localisation import (
    OfferLocalisationModel,
)
from infrastructure.factories.datetime_utils import as_aware
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)

_MAIN_LOCALISATION_KWARGS = {
    "area": ("area", GeographicalArea.EUROPE.value),
    "country": ("country", "FRA"),
    "region": ("region", "11"),
    "department": ("department", "75"),
    "location_label": ("label", ""),
    "latitude": ("latitude", None),
    "longitude": ("longitude", None),
}


class OfferDjangoFactory(DjangoModelFactory):
    class Meta:
        model = OfferModel
        skip_postgeneration_save = True

    id = factory.LazyFunction(uuid4)
    source = factory.SubFactory(SourceDjangoFactory)
    reference = factory.LazyFunction(lambda: str(uuid4()))
    verse = Verse.FPE.value
    title = "Test Offer Title"
    profile = "Test profile description"
    mission = "Test mission description"
    categories = factory.LazyFunction(lambda: [Category.A.value])
    organization = "Test Organization"
    publication_date = datetime(2024, 1, 15, tzinfo=UTC)
    end_publication_date = datetime(2025, 1, 15, tzinfo=UTC)
    beginning_date = datetime(2024, 12, 31, tzinfo=UTC)
    processing = False
    processed_at = None
    archived_at = None

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Flat kwargs (department="69", latitude=…) describe the main localisation
        main = {
            field: kwargs.pop(kwarg, default)
            for kwarg, (field, default) in _MAIN_LOCALISATION_KWARGS.items()
        }
        localisations = kwargs.pop("localisations", None)
        if localisations is None:
            localisations = [main] if main["area"] and main["country"] else []
        offer = super()._create(model_class, *args, **kwargs)
        OfferLocalisationModel.objects.bulk_create(
            OfferLocalisationModel(
                id=uuid4(),
                offer=offer,
                position=position,
                **{
                    field: value
                    for field, value in localisation.items()
                    # label is the only non nullable optional field
                    if value is not None or field != "label"
                },
            )
            for position, localisation in enumerate(localisations)
        )
        return offer

    @factory.post_generation
    def updated_at(self, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        OfferModel.objects.filter(id=self.id).update(updated_at=as_aware(extracted))
        self.refresh_from_db()
