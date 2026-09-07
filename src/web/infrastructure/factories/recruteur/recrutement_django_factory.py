from datetime import datetime
from uuid import uuid4

import factory
from factory.django import DjangoModelFactory

from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import AgentRecrutementRole
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
    RecrutementModel,
)
from infrastructure.factories.identite.agent_django_factory import (
    AgentDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)


class RecrutementDjangoFactory(DjangoModelFactory):
    class Meta:
        model = RecrutementModel
        skip_postgeneration_save = True

    class Params:
        offre_archivee = factory.Trait(
            offre=factory.SubFactory(
                OfferDjangoFactory, archived_at=datetime(2024, 1, 1)
            )
        )

    offre = factory.SubFactory(OfferDjangoFactory)
    organisme = factory.SubFactory(OrganismeDjangoFactory)
    ordre_etapes = factory.LazyFunction(list)

    agent_link = factory.RelatedFactory(
        "infrastructure.factories.recruteur.recrutement_django_factory."
        "RecrutementAgentDjangoFactory",
        factory_related_name="recrutement",
    )

    @factory.post_generation
    def etapes(self, create, extracted, **kwargs):
        if not create:
            return
        etapes = (
            extracted
            if extracted is not None
            else EtapeRecrutementFactory.create_entity_batch()
        )
        if kwargs.get("persist", True):
            for etape in etapes:
                EtapeModel(
                    id=etape.entity_id,
                    recrutement=self,
                    categorie=etape.categorie.value,
                    nom=etape.nom,
                    ordre_candidatures=[str(c) for c in etape.candidatures]
                    if etape.candidatures
                    else None,
                ).save()
        self.ordre_etapes = [str(etape.entity_id) for etape in etapes]
        self.save(update_fields=["ordre_etapes"])


class EtapeDjangoFactory(DjangoModelFactory):
    class Meta:
        model = EtapeModel

    id = factory.LazyFunction(uuid4)
    recrutement = factory.SubFactory(RecrutementDjangoFactory)
    categorie = CategorieEtapeRecrutement.EN_COURS.value
    nom = "Entretien"
    ordre_candidatures = None


class RecrutementAgentDjangoFactory(DjangoModelFactory):
    class Meta:
        model = RecrutementAgentModel

    id = factory.LazyFunction(uuid4)
    recrutement = factory.SubFactory(RecrutementDjangoFactory)
    agent = factory.SubFactory(AgentDjangoFactory)
    role = AgentRecrutementRole.CONTRIBUTEUR.value
