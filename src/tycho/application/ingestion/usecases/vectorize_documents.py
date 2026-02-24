import uuid
from typing import Any, Dict, Union

from django.db import transaction

from domain.entities.concours import Concours
from domain.entities.corps import Corps
from domain.entities.document import Document, DocumentType
from domain.entities.offer import Offer
from domain.entities.vectorized_document import VectorizedDocument
from domain.exceptions.document_error import UnsupportedDocumentTypeError
from domain.interfaces.entity_interface import IEntity
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.repositories.corps_repository_interface import ICorpsRepository
from domain.repositories.offers_repository_interface import IOffersRepository
from domain.repositories.vector_repository_interface import IVectorRepository
from domain.services.embedding_generator_interface import IEmbeddingGenerator
from domain.services.logger_interface import ILogger
from domain.services.text_extractor_interface import ITextExtractor


class VectorizeDocumentsUsecase:
    def __init__(
        self,
        vector_repository: IVectorRepository,
        text_extractor: ITextExtractor,
        embedding_generator: IEmbeddingGenerator,
        logger: ILogger,
        repository_factory: Union[
            ICorpsRepository, IConcoursRepository, IOffersRepository
        ],
    ):
        self.vector_repository = vector_repository
        self.text_extractor = text_extractor
        self.embedding_generator = embedding_generator
        self.logger = logger
        self.repository_factory = repository_factory

    def execute(self, document_type: DocumentType, limit: int = 250) -> Dict[str, Any]:
        self.logger.info(
            "Starting vectorization of %d document type: %s,", limit, document_type
        )

        results: Dict[str, Any] = {
            "processed": 0,
            "vectorized": 0,
            "errors": 0,
            "error_details": [],
        }

        vectorized_documents = []
        successful_sources = []
        failed_sources = []

        repository = self.repository_factory.get_repository(document_type)
        sources = repository.get_pending_processing(limit=limit)

        for source in sources:
            try:
                vectorized_documents.append(self.vectorize_single_source(source))
                successful_sources.append(source)
            except Exception as e:
                self.logger.error("Failed to vectorize source: %s", str(e))
                failed_sources.append(source)
                results["errors"] += 1
                results["error_details"].append(
                    {
                        "error": "Failed to vectorize source",
                        "source_type": type(source).__name__,
                        "source_id": getattr(source, "id", "unknown"),
                        "exception": str(e),
                    }
                )
        results["vectorized"] = len(successful_sources)

        with transaction.atomic():
            if successful_sources:
                try:
                    self.vector_repository.upsert_batch(
                        vectorized_documents, document_type
                    )
                    repository.mark_as_processed(successful_sources)
                    results["processed"] = len(successful_sources)
                except Exception as e:
                    self.logger.error(
                        "Failed to save successful vectorized sources: %s", str(e)
                    )
                    results["errors"] += len(successful_sources)
                    results["error_details"].append(
                        {
                            "error": "Failed to save successful vectorized sources",
                            "exception": str(e),
                        }
                    )

            if failed_sources:
                try:
                    repository.mark_as_pending(failed_sources)
                except Exception as e:
                    self.logger.error("Failed to save failed sources: %s", str(e))
                    results["errors"] += len(failed_sources)
                    results["error_details"].append(
                        {
                            "error": "Failed to save failed vectorized sources",
                            "exception": str(e),
                        }
                    )

        return results

    def vectorize_single_source(
        self, source: Union[Document, IEntity]
    ) -> VectorizedDocument:
        content = self.text_extractor.extract_content(source)
        metadata = self.text_extractor.extract_metadata(source)

        embedding = self.embedding_generator.generate_embedding(content)

        if isinstance(source, Document):
            entity_id = str(source.id)
            document_type = source.type
        elif isinstance(source, Corps):
            entity_id = str(source.id)
            document_type = DocumentType.CORPS
        elif isinstance(source, Concours):
            entity_id = str(source.id)
            document_type = DocumentType.CONCOURS
        elif isinstance(source, Offer):
            entity_id = str(source.id)
            document_type = DocumentType.OFFERS
        else:
            raise UnsupportedDocumentTypeError(type(source).__name__)

        # Ensure entity_id is not None for VectorizedDocument
        if entity_id is None:
            raise ValueError("Entity ID cannot be None for vectorization")

        return VectorizedDocument(
            entity_id=uuid.UUID(entity_id),
            document_type=document_type,
            content=content,
            embedding=embedding,
            metadata=metadata,
        )
