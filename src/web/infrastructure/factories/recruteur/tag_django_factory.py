from uuid import uuid4

import factory
from factory.django import DjangoModelFactory

from infrastructure.django_apps.recruteur.models.tag import (
    CandidatureTagModel,
    NoteTagModel,
    RecrutementAgentTagModel,
    TagCategory,
    TagModel,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.recruteur.note_django_factory import NoteDjangoFactory
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
)


class TagDjangoFactory(DjangoModelFactory):
    class Meta:
        model = TagModel

    id = factory.LazyFunction(uuid4)
    organisme = factory.SubFactory(OrganismeDjangoFactory)
    name = factory.Sequence(lambda n: f"Étiquette {n}")
    category = TagCategory.CANDIDATURE


class CandidatureTagDjangoFactory(DjangoModelFactory):
    class Meta:
        model = CandidatureTagModel

    id = factory.LazyFunction(uuid4)
    tag = factory.SubFactory(
        TagDjangoFactory,
        category=TagCategory.CANDIDATURE,
        organisme=factory.SelfAttribute("..candidature.etape.recrutement.organisme"),
    )
    candidature = factory.SubFactory(CandidatureDjangoFactory)


class RecrutementAgentTagDjangoFactory(DjangoModelFactory):
    class Meta:
        model = RecrutementAgentTagModel

    id = factory.LazyFunction(uuid4)
    tag = factory.SubFactory(
        TagDjangoFactory,
        category=TagCategory.RECRUTEMENT_AGENT,
        organisme=factory.SelfAttribute("..recrutement_agent.recrutement.organisme"),
    )
    recrutement_agent = factory.SubFactory(RecrutementAgentDjangoFactory)


class NoteTagDjangoFactory(DjangoModelFactory):
    class Meta:
        model = NoteTagModel

    id = factory.LazyFunction(uuid4)
    tag = factory.SubFactory(
        TagDjangoFactory,
        category=TagCategory.NOTE,
        organisme=factory.SelfAttribute(
            "..note.candidature.etape.recrutement.organisme"
        ),
    )
    note = factory.SubFactory(NoteDjangoFactory)
