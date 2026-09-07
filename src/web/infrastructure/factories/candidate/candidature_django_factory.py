from uuid import uuid4

import factory
from factory.django import DjangoModelFactory

from domain.candidate.value_objects.statut_candidature import StatutCandidature
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.factories.identite.candidat_django_factory import (
    CandidatDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
)


class CandidatureDjangoFactory(DjangoModelFactory):
    class Meta:
        model = CandidatureModel

    id = factory.LazyFunction(uuid4)
    candidat = factory.SubFactory(CandidatDjangoFactory)
    etape = factory.SubFactory(EtapeDjangoFactory)
    statut = StatutCandidature.INITIAL.value
    documents = None
