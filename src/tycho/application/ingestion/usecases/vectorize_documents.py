import uuid
from typing import Any, Dict, List, Union

from domain.entities.concours import Concours
from domain.entities.corps import Corps
from domain.entities.document import Document, DocumentType
from domain.entities.offer import Offer
from domain.entities.vectorized_document import VectorizedDocument
from domain.exceptions.document_error import UnsupportedDocumentTypeError
from domain.interfaces.entity_interface import IEntity
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
    ):
        self.vector_repository = vector_repository
        self.text_extractor = text_extractor
        self.embedding_generator = embedding_generator
        self.logger = logger

    def execute(self, sources: List[Union[Document, IEntity]]) -> Dict[str, Any]:
        self.logger.info(f"Starting vectorization of {len(sources)} sources")

        results: Dict[str, Any] = {
            "processed": 0,
            "vectorized": 0,
            "errors": 0,
            "error_details": [],
        }

        for source in sources:
            try:
                self._vectorize_single_source(source)
                results["vectorized"] += 1
            except Exception as e:
                self.logger.error(f"Failed to vectorize source: {str(e)}")
                results["errors"] += 1
                results["error_details"].append(
                    {
                        "source_type": type(source).__name__,
                        "source_id": getattr(source, "id", "unknown"),
                        "error": str(e),
                    }
                )
            finally:
                results["processed"] += 1

        self.logger.info(f"Vectorization completed: {results}")
        return results

    def _vectorize_single_source(
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
