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
