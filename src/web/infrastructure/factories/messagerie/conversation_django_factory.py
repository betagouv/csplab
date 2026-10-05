from uuid import uuid4

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from infrastructure.django_apps.messagerie.models import (
    ConversationLectureModel,
    ConversationModel,
    MessageDocumentModel,
    MessageModel,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.candidate.document_django_factory import (
    DocumentDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)


class ConversationDjangoFactory(DjangoModelFactory[ConversationModel]):
    class Meta:
        model = ConversationModel

    id = factory.LazyFunction(uuid4)
    candidature = factory.SubFactory(CandidatureDjangoFactory)
    objet = factory.Faker("sentence", nb_words=4, locale="fr_FR")


class MessageDocumentDjangoFactory(DjangoModelFactory[MessageDocumentModel]):
    class Meta:
        model = MessageDocumentModel

    id = factory.LazyFunction(uuid4)
    document = factory.SubFactory(
        DocumentDjangoFactory,
        candidature=factory.SelfAttribute("..message.conversation.candidature"),
    )


class MessageDjangoFactory(DjangoModelFactory[MessageModel]):
    class Meta:
        model = MessageModel

    class Params:
        par_candidat = factory.Trait(
            auteur=factory.SelfAttribute(
                "conversation.candidature.candidat.utilisateur"
            ),
        )
        with_document = factory.Trait(
            piece_jointe=factory.RelatedFactory(
                MessageDocumentDjangoFactory, factory_related_name="message"
            ),
        )

    id = factory.LazyFunction(uuid4)
    conversation = factory.SubFactory(ConversationDjangoFactory)
    contenu = factory.Faker("paragraph", locale="fr_FR")
    auteur = factory.SubFactory(UtilisateurDjangoFactory)


class ConversationLectureDjangoFactory(DjangoModelFactory[ConversationLectureModel]):
    class Meta:
        model = ConversationLectureModel

    id = factory.LazyFunction(uuid4)
    conversation = factory.SubFactory(ConversationDjangoFactory)
    utilisateur = factory.SubFactory(UtilisateurDjangoFactory)
    read_at = factory.LazyFunction(timezone.now)
