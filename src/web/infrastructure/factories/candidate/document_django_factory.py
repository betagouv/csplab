from uuid import uuid4

import factory
from factory.django import DjangoModelFactory

from infrastructure.django_apps.candidate.enums.type_document import TypeDocument
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)


class DocumentDjangoFactory(DjangoModelFactory):
    class Meta:
        model = DocumentModel

    id = factory.LazyFunction(uuid4)
    candidature = factory.SubFactory(CandidatureDjangoFactory)
    type_document = TypeDocument.CV.value
    fichier = factory.django.FileField(filename="test.pdf", data=b"%PDF-1.4\n%test")
    nom_original = "test.pdf"
    content_type = "application/pdf"
    taille = 13
    depose_par = factory.SubFactory(UtilisateurDjangoFactory)
