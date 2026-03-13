import random
from typing import List, Optional
from uuid import UUID, uuid4

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
        embedding_dimensions: int = 1536,  # Default to pgvector dimensions
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
                metadata = {
                    "verse": random.choice(["FPE", "FPT", "FPH"]),
                    "contract_type": random.choice(
                        [None, "TITULAIRE_CONTRACTUEL", "CONTRACTUELS", "TERRITORIAL"]
                    ),
                    "localisation": random.choice(
                        [None, "FRA-11-75", "FRA-84-13", "FRA-32-69"]
                    ),
                }

        entity = VectorizedDocument(
            entity_id=entity_id,
            document_type=document_type,
            content=content,
            embedding=embedding,
            metadata=metadata,
        )

        # Return the entity directly instead of saving to pgvector
        # The caller should use the vector repository (Qdrant) to save
        return entity

    @staticmethod
    def create_batch(
        size: int,
        **kwargs,
    ) -> List[VectorizedDocument]:
        return [VectorizedDocumentFactory.create(**kwargs) for _ in range(size)]
