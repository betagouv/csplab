import random
from typing import List, Optional
from uuid import UUID, uuid4

from faker import Faker

from domain.entities.document import DocumentType
from domain.entities.vectorized_document import VectorizedDocument
from infrastructure.django_apps.shared.models.vectorized_document import (
    VectorizedDocumentModel,
)

fake = Faker()


class VectorizedDocumentFactory:
    @staticmethod
    def create(
        entity_id: Optional[UUID] = None,
        document_type: DocumentType = DocumentType.OFFERS,
    ) -> VectorizedDocumentModel:
        if entity_id is None:
            entity_id = uuid4()
        elif isinstance(entity_id, str):
            entity_id = UUID(entity_id)

        entity = VectorizedDocument(
            entity_id=entity_id,
            document_type=document_type,
            content=fake.paragraph(),
            embedding=[random.random() for i in range(3072)],
            metadata={
                "verse": "FPE",
                "category": None,
                "localisation": {"region": "11", "country": "FRA", "department": "93"},
            },
        )

        vectorized_doc = VectorizedDocumentModel.from_entity(entity)
        vectorized_doc.save()

        return vectorized_doc

    @staticmethod
    def create_batch(
        size: int,
        **kwargs,
    ) -> List[VectorizedDocumentModel]:
        return [VectorizedDocumentFactory.create(**kwargs) for _ in range(size)]
