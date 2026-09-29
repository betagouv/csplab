from uuid import uuid4

import factory
from factory.django import DjangoModelFactory

from infrastructure.django_apps.ingestion.models.talentsoft_organisme import (
    TalentsoftOrganismeModel,
)


class TalentsoftOrganismeDjangoFactory(DjangoModelFactory):
    class Meta:
        model = TalentsoftOrganismeModel

    id = factory.LazyFunction(uuid4)
    entity_code = factory.Sequence(lambda n: f"ENT-{n}")
    code = factory.Sequence(lambda n: n)
    name = factory.Faker("company", locale="fr_FR")
    description = factory.Faker("paragraph", locale="fr_FR")
    url = factory.Faker("url")
    phone_number = factory.Faker("phone_number", locale="fr_FR")
    post_code = factory.Faker("postcode", locale="fr_FR")
    latitude = factory.Faker("pyfloat", min_value=-90, max_value=90)
    longitude = factory.Faker("pyfloat", min_value=-180, max_value=180)
    parent_name = factory.Faker("company", locale="fr_FR")
    logo_url = factory.Faker("image_url")
    max_delay_for_consent = factory.Faker("pyint", min_value=1, max_value=365)
    retention_period = factory.Faker("pyint", min_value=1, max_value=60)
    general_conditions = factory.Faker("paragraph", locale="fr_FR")
    personal_data_consent = factory.Faker("paragraph", locale="fr_FR")
