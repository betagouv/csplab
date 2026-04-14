import random
from typing import List, Optional
from uuid import UUID, uuid4

from django.conf import settings
from faker import Faker

from domain.entities.document import DocumentType
from domain.entities.vectorized_document import VectorizedDocument

fake = Faker()


class VectorizedDocumentFactory:
    @staticmethod
    def create(
        entity_id: Optional[UUID] = None,
        document_type: DocumentType = DocumentType.OFFERS,
        content: Optional[str] = None,
        embedding: Optional[List[float]] = None,
        metadata: Optional[dict] = None,
        embedding_dimensions: int = settings.EMBEDDING_DIMENSION,
    ) -> VectorizedDocument:
        if entity_id is None:
            entity_id = uuid4()
        elif isinstance(entity_id, str):
            entity_id = UUID(entity_id)

        if content is None:
            content = fake.paragraph()

        if embedding is None:
            embedding = [random.random() for i in range(embedding_dimensions)]

        if metadata is None:
            if document_type == DocumentType.CONCOURS:
                metadata = {
                    "category": random.choice(
                        ["APLUS", "A", "B", "C", "HORS_CATEGORIE"]
                    ),
                    "ministry": random.choice(
                        ["MAA", "MESRI", "MEF", "MEN", "MSS", "MC", "MJ", "MI", "MTE"]
                    ),
                    "access_modality": random.choice(
                        [
                            [],
                            ["Concours externe"],
                            ["Concours interne"],
                            ["Concours externe", "Concours interne"],
                            ["3ème concours"],
                            ["Sans concours"],
                        ]
                    ),
                }
            else:  # DocumentType.OFFERS
                localisation_choices = [
                    None,
                    {
                        "region": "11",
                        "country": "FRA",
                        "department": "75",
                    },
                    {
                        "region": "84",
                        "country": "FRA",
                        "department": "13",
                    },
                    {
                        "region": "32",
                        "country": "FRA",
                        "department": "60",
                    },
                    {
                        "region": "44",
                        "country": "FRA",
                        "department": "67",
                    },
                    {
                        "region": "93",
                        "country": "FRA",
                        "department": "06",
                    },
                ]

                metadata = {
                    "verse": random.choice(["FPE", "FPT", "FPH"]),
                    "category": None,
                    "localisation": random.choice(localisation_choices),
                }

        entity = VectorizedDocument(
            entity_id=entity_id,
            document_type=document_type,
            content=content,
            embedding=embedding,
            metadata=metadata,
        )

        return entity

    @staticmethod
    def create_batch(
        size: int,
        **kwargs,
    ) -> List[VectorizedDocument]:
        return [VectorizedDocumentFactory.create(**kwargs) for _ in range(size)]
