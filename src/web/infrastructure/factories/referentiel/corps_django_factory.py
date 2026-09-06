from uuid import uuid4

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from referentiel.value_objects.category import Category
from referentiel.value_objects.ministry import Ministry

from infrastructure.django_apps.referentiel.models.corps import CorpsModel


class CorpsDjangoFactory(DjangoModelFactory):
    class Meta:
        model = CorpsModel
        skip_postgeneration_save = True

    id = factory.LazyFunction(uuid4)
    code = factory.Faker("word")
    category = Category.A.value
    ministry = Ministry.MI.value
    diploma_level = None
    short_label = factory.Faker("job")
    long_label = factory.Faker("sentence")
    access_modalities = factory.LazyFunction(list)
    processing = False
    processed_at = None
    archived_at = None

    @factory.post_generation
    def updated_at(self, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        CorpsModel.objects.filter(id=self.id).update(
            updated_at=timezone.make_aware(extracted)
        )
        self.refresh_from_db()
