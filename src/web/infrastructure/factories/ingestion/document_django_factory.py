from uuid import uuid4

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from domain.ingestion.entities.document import DocumentType
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument


class DocumentDjangoFactory(DjangoModelFactory):
    class Meta:
        model = RawDocument
        skip_postgeneration_save = True

    id = factory.LazyFunction(uuid4)
    created_at = factory.LazyFunction(timezone.now)
    external_id = factory.Sequence(lambda n: f"test_doc_{n}")
    document_type = DocumentType.OFFERS.value
    raw_data = factory.LazyAttribute(
        lambda o: {
            "id": o.external_id,
            "name": f"Test {o.document_type}",
            "description": f"Test document of type {o.document_type}",
        }
    )
    processing = False
    processed_at = None
    error_msg = None

    @factory.post_generation
    def updated_at(self, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        RawDocument.objects.filter(id=self.id).update(
            updated_at=timezone.make_aware(extracted)
        )
        self.refresh_from_db()
