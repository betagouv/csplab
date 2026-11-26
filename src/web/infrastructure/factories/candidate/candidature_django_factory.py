from uuid import uuid4

import factory
from factory.django import DjangoModelFactory

from domain.candidate.value_objects.statut_candidature import StatutCandidature
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus
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


class EtapeRefusDjangoFactory(EtapeDjangoFactory):
    class Meta:
        django_get_or_create = ("recrutement", "categorie")

    categorie = CategorieEtapeRecrutement.REFUS.value
    nom = "Refus"


class CandidatureDjangoFactory(DjangoModelFactory):
    class Meta:
        model = CandidatureModel

    class Params:
        refusee = factory.Trait(
            etape=factory.SubFactory(EtapeRefusDjangoFactory),
            statut=StatutCandidature.SOUMISE.value,
            motif_refus=MotifRefus.EXPERIENCE_INSUFFISANTE.value,
        )

    id = factory.LazyFunction(uuid4)
    candidat = factory.SubFactory(CandidatDjangoFactory)
    etape = factory.SubFactory(EtapeDjangoFactory)
    statut = StatutCandidature.INITIAL.value
    documents = None


def create_recrutement_with_candidature(
    organisme=None, candidature_kwargs=None, **recrutement_kwargs
):
    if organisme is not None:
        recrutement_kwargs["organisme"] = organisme
    recrutement = RecrutementDjangoFactory(**recrutement_kwargs)
    candidature = CandidatureDjangoFactory(
        etape__recrutement=recrutement, **(candidature_kwargs or {})
    )
    return recrutement, candidature


def create_recrutement_and_candidature_for_agent(
    role=AgentOrganismeRole.SUPERVISEUR, utilisateur=None, candidature_kwargs=None
):
    agent, organisme = create_organisme_with_agent(role=role, utilisateur=utilisateur)
    recrutement, candidature = create_recrutement_with_candidature(
        organisme, candidature_kwargs=candidature_kwargs
    )
    return agent, organisme, recrutement, candidature
