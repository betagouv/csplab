from uuid import uuid4

import factory
from factory.django import DjangoModelFactory
from referentiel.value_objects.source_type import SourceType

from infrastructure.django_apps.ingestion.models.source import SourceModel


class SourceDjangoFactory(DjangoModelFactory):
    class Meta:
        model = SourceModel

    source_id = factory.LazyFunction(uuid4)
    slug = factory.Sequence(lambda n: f"source-{n}")
    type = SourceType.TALENTSOFT.value
    client_id_front = factory.Faker("word")
    client_id_back = factory.Faker("word")
    base_url_front = factory.Faker("url")
    base_url_back = factory.Faker("url")
