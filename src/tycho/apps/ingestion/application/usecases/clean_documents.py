"""CleanDocuments usecase."""

from typing import Any, Dict, List, cast

from core.entities.corps import Corps
from core.entities.document import DocumentType
from core.interfaces.entity_interface import IEntity
from core.repositories.document_repository_interface import IDocumentRepository
from core.repositories.repository_factory_interface import IRepositoryFactory
from core.services.document_cleaner_interface import IDocumentCleaner
from core.services.logger_interface import ILogger


class CleanDocumentsUsecase:
    """Usecase for cleaning and processing raw documents into typed entities."""

    def __init__(
        self,
        document_repository: IDocumentRepository,
        document_cleaner: IDocumentCleaner[IEntity],
        repository_factory: IRepositoryFactory,
        logger: ILogger,
    ):
        """Initialize with dependencies."""
        self.document_repository = document_repository
        self.document_cleaner = document_cleaner
        self.repository_factory = repository_factory
        self.logger = logger.get_logger(
            "INGESTION::APPLICATION::CleanDocumentsUsecase::execute"
        )

    def execute(self, input_data: DocumentType) -> Dict[str, Any]:
        """Execute the usecase to clean documents and return processing results."""
        raw_documents = self.document_repository.fetch_by_type(input_data)
        self.logger.info(
            f"Fetched {len(raw_documents)} raw documents of type {input_data}"
        )

        cleaned_entities = self.document_cleaner.clean(raw_documents)
        self.logger.info(
            f"Cleaned {len(cleaned_entities)} entities from "
            f"{len(raw_documents)} raw documents"
        )

        if not cleaned_entities:
            return {
                "processed": len(raw_documents),
                "cleaned": 0,
                "created": 0,
                "updated": 0,
                "errors": 0,
            }

        repository = self.repository_factory.get_repository(input_data)
        cleaned_corps = cast(List[Corps], cleaned_entities)
        save_result = repository.save_batch(cleaned_corps)

        self.logger.info(f"Saved entities: {save_result}")

        return {
            "processed": len(raw_documents),
            "cleaned": len(cleaned_entities),
            "created": save_result.get("created", 0),
            "updated": save_result.get("updated", 0),
            "errors": save_result.get("errors", 0),
        }
