from uuid import uuid4

import factory
from factory.django import DjangoModelFactory, Password

from infrastructure.django_apps.users.models import UserModel
from infrastructure.factories.identite.utilisateur_factory import DEFAULT_PASSWORD


class UtilisateurDjangoFactory(DjangoModelFactory):
    class Meta:
        model = UserModel
        skip_postgeneration_save = True

    username = factory.LazyFunction(uuid4)
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.org")
    first_name = factory.Faker("first_name", locale="fr_FR")
    last_name = factory.Faker("last_name", locale="fr_FR")
    is_staff = False
    is_superuser = False
    password = Password(DEFAULT_PASSWORD)

    @factory.post_generation
    def sources(self, create, extracted, **kwargs):
        if create and extracted:
            self.sources.add(*extracted)
