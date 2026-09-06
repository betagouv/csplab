from uuid import uuid4

import factory
from factory.django import DjangoModelFactory
from faker import Faker

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import (
    OrganismeAgentModel,
    OrganismeModel,
)
from infrastructure.factories.identite.agent_django_factory import (
    AgentDjangoFactory,
)
from infrastructure.mappers.organisme_recruteur_mapper import OrganismeRecruteurMapper

_fake = Faker("fr_FR")


class OrganismeDjangoFactory(DjangoModelFactory):
    class Meta:
        model = OrganismeModel
        skip_postgeneration_save = True

    class Params:
        with_agent = factory.Trait(
            agent_liaison=factory.RelatedFactory(
                "infrastructure.factories.identite.organisme_django_factory."
                "OrganismeAgentDjangoFactory",
                factory_related_name="organisme",
            )
        )

    id = factory.LazyFunction(uuid4)
    nom = "Ministère de l'Économie, des Finances et de la Relance"
    versant = "FPE"
    siret = factory.LazyFunction(lambda: _fake.siret().replace(" ", ""))
    gestion_ats = False

    @factory.post_generation
    def etapes(self, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        self.etapes = OrganismeRecruteurMapper().from_domain(extracted)
        self.save(update_fields=["etapes"])


class OrganismeAgentDjangoFactory(DjangoModelFactory):
    class Meta:
        model = OrganismeAgentModel

    id = factory.LazyFunction(uuid4)
    organisme = factory.SubFactory(OrganismeDjangoFactory)
    agent = factory.SubFactory(AgentDjangoFactory)
    role = AgentOrganismeRole.MEMBRE.value


def create_organisme_with_agent(
    role=None,
    utilisateur=None,
    intitule_poste=None,
    **organisme_kwargs,
):
    """Replaces the old OrganismeFactory.create_model_with_agent().

    Built on the `with_agent` trait, but returns (agent, organisme) since
    every call site needs both. Unlike the old factory, the agent is
    always linked to the organisme (no silent unlinked-agent case
    depending on whether role was passed).
    """
    agent_overrides = {}
    if utilisateur is not None:
        agent_overrides["agent_liaison__agent__utilisateur"] = utilisateur
    if intitule_poste is not None:
        agent_overrides["agent_liaison__agent__intitule_poste"] = intitule_poste

    organisme = OrganismeDjangoFactory(
        with_agent=True,
        agent_liaison__role=(role or AgentOrganismeRole.MEMBRE).value,
        **agent_overrides,
        **organisme_kwargs,
    )
    agent = organisme.agents_liaisons.get().agent
    return agent, organisme
