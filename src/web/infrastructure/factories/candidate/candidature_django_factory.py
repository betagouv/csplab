from uuid import uuid4

import factory
from factory.django import DjangoModelFactory

from domain.candidate.value_objects.statut_candidature import StatutCandidature
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.factories.identite.candidat_django_factory import (
    CandidatDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementDjangoFactory,
)


class CandidatureDjangoFactory(DjangoModelFactory):
    class Meta:
        model = CandidatureModel

    id = factory.LazyFunction(uuid4)
    candidat = factory.SubFactory(CandidatDjangoFactory)
    etape = factory.SubFactory(EtapeDjangoFactory)
    statut = StatutCandidature.INITIAL.value
    documents = None


def create_recrutement_and_candidature_for_agent(
    role=AgentOrganismeRole.SUPERVISEUR, utilisateur=None
):
    agent, organisme = create_organisme_with_agent(role=role, utilisateur=utilisateur)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(etape__recrutement=recrutement)
    return agent, organisme, recrutement, candidature
