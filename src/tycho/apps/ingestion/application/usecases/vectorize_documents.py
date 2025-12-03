"""VectorizeDocuments usecase."""

from datetime import datetime
from typing import Any, Dict, List, Union

from core.entities.corps import Corps
from core.entities.document import Document
from core.entities.vectorized_document import VectorizedDocument
from core.interfaces.entity_interface import IEntity
from core.repositories.vector_repository_interface import IVectorRepository
from core.services.embedding_generator_interface import IEmbeddingGenerator
from core.services.logger_interface import ILogger
from core.services.text_extractor_interface import ITextExtractor


class VectorizeDocumentsUsecase:
    """Usecase for vectorizing documents or clean entities."""

    def __init__(
        self,
        vector_repository: IVectorRepository,
        text_extractor: ITextExtractor,
        embedding_generator: IEmbeddingGenerator,
        logger: ILogger,
    ):
        """Initialize with dependencies."""
        self.vector_repository = vector_repository
        self.text_extractor = text_extractor
        self.embedding_generator = embedding_generator
        self.logger = logger.get_logger(
            "INGESTION::APPLICATION::VectorizeDocumentsUsecase::execute"
        )

    def execute(self, sources: List[Union[Document, IEntity]]) -> Dict[str, Any]:
        """Execute the usecase to vectorize documents or entities."""
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
        """Vectorize a single document or entity."""
        # Extract content and metadata
        content = self.text_extractor.extract_content(source)
        metadata = self.text_extractor.extract_metadata(source)

        # Generate embedding
        embedding = self.embedding_generator.generate_embedding(content)

        # Determine document_id based on source type
        if isinstance(source, Document):
            document_id = source.id
        elif isinstance(source, Corps):
            document_id = source.id
        else:
            raise ValueError(f"Unsupported source type: {type(source)}")

        # Create vectorized document
        vectorized_doc = VectorizedDocument(
            id=0,  # Will be set by the repository
            document_id=document_id,
            content=content,
            embedding=embedding,
            metadata=metadata,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # Store in repository
        return self.vector_repository.store_embedding(vectorized_doc)
