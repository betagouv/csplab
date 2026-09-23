from uuid import uuid4

import factory
from factory.django import DjangoModelFactory
from faker import Faker
from referentiel.value_objects.category import Category
from referentiel.value_objects.label import Label
from referentiel.value_objects.ministry import Ministry

from infrastructure.django_apps.referentiel.models.corps import CorpsModel
from infrastructure.factories.datetime_utils import as_aware

fake = Faker()


class CorpsDjangoFactory(DjangoModelFactory):
    class Meta:
        model = CorpsModel
        skip_postgeneration_save = True

    id = factory.LazyFunction(uuid4)
    code = factory.Faker("word")
    category = Category.A.value
    ministry = Ministry.MI.value
    diploma_level = None
    short_label = factory.LazyFunction(
        lambda: fake.job()[: Label.MAX_SHORT_LABEL_LENGTH]
    )
    long_label = factory.Faker("text", max_nb_chars=Label.MAX_LONG_LABEL_LENGTH)
    access_modalities = factory.LazyFunction(list)
    processing = False
    processed_at = None
    archived_at = None

    @factory.post_generation
    def updated_at(self, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        CorpsModel.objects.filter(id=self.id).update(updated_at=as_aware(extracted))
        self.refresh_from_db()
