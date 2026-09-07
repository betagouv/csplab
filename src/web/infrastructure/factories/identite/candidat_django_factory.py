import factory
from factory.django import DjangoModelFactory

from infrastructure.django_apps.users.models import ProfilCandidatModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)


class CandidatDjangoFactory(DjangoModelFactory):
    class Meta:
        model = ProfilCandidatModel

    utilisateur = factory.SubFactory(UtilisateurDjangoFactory)
    resume = factory.Faker("paragraph", locale="fr_FR")
