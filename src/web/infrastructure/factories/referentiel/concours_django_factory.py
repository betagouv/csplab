from uuid import uuid4

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from referentiel.value_objects.category import Category
from referentiel.value_objects.ministry import Ministry

from infrastructure.django_apps.referentiel.models.concours import ConcoursModel
from infrastructure.factories.referentiel.concours_factory import NorProvider

factory.Faker.add_provider(NorProvider)


class ConcoursDjangoFactory(DjangoModelFactory):
    class Meta:
        model = ConcoursModel
        skip_postgeneration_save = True

    id = factory.LazyFunction(uuid4)
    corps = "Test Corps"
    grade = "Test Grade"
    nor_original = factory.Faker("nor")
    nor_list = factory.LazyFunction(list)
    category = Category.A.value
    ministry = Ministry.MI.value
    access_modality = factory.LazyFunction(list)
    written_exam_date = None
    open_position_number = 10
    processing = False
    processed_at = None
    archived_at = None

    @factory.post_generation
    def updated_at(self, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        ConcoursModel.objects.filter(id=self.id).update(
            updated_at=timezone.make_aware(extracted)
        )
        self.refresh_from_db()
