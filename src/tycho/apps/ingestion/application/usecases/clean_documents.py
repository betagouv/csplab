"""CleanDocuments usecase."""

from typing import Any, Dict

from core.entities.document import DocumentType
from core.interfaces.entity_interface import IEntity
from core.repositories.document_repository_interface import IDocumentRepository
from core.services.document_cleaner_interface import IDocumentCleaner
from core.services.logger_interface import ILogger


class CleanDocumentsUsecase:
    """Usecase for cleaning and processing raw documents into typed entities."""

    def __init__(
        self,
        document_repository: IDocumentRepository,
        document_cleaner: IDocumentCleaner[IEntity],
        logger: ILogger,
    ):
        """Initialize with dependencies."""
        self.document_repository = document_repository
        self.document_cleaner = document_cleaner
        self.logger = logger

    def execute(self, input_data: DocumentType) -> Dict[str, Any]:
        """Execute the usecase to clean documents and return processing results."""
        try:
            # Fetch raw documents
            raw_documents = self.document_repository.fetch_by_type(input_data)

            # Clean documents using the injected cleaner
            cleaned_entities = self.document_cleaner.clean(raw_documents)

            # TODO: Add repository factory to get appropriate repository for entity type
            # repository = self.repository_factory.get_repository(input_data)
            # result = repository.save_batch(cleaned_entities)

            # Placeholder result for now
            result = {
                "processed": len(raw_documents),
                "cleaned": len(cleaned_entities),
                "created": 0,
                "updated": 0,
                "errors": 0,
            }

            return result

        except Exception:
            logger_instance = self.logger.get_logger(
                "INGESTION::APPLICATION::CleanDocumentsUsecase::execute"
            )
            logger_instance.error("Error cleaning documents")
            raise
