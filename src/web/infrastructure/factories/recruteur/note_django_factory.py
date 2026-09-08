from uuid import uuid4

import factory
from factory.django import DjangoModelFactory

from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory


class NoteDjangoFactory(DjangoModelFactory):
    class Meta:
        model = NoteModel

    id = factory.LazyFunction(uuid4)
    candidature = factory.SubFactory(CandidatureDjangoFactory)
    publie_par = factory.SubFactory(AgentDjangoFactory)
    message = factory.Faker("sentence", locale="fr_FR")
