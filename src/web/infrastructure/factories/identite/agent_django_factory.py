import factory
from factory.django import DjangoModelFactory

from infrastructure.django_apps.users.models import ProfilAgentModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)


class AgentDjangoFactory(DjangoModelFactory):
    class Meta:
        model = ProfilAgentModel

    utilisateur = factory.SubFactory(UtilisateurDjangoFactory)
    intitule_poste = factory.Faker("job", locale="fr_FR")
