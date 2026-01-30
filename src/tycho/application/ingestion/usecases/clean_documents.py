"""CleanDocuments usecase."""

from typing import Any, Dict, List, cast

from domain.entities.document import DocumentType
from domain.interfaces.entity_interface import IEntity
from domain.repositories.document_repository_interface import IDocumentRepository
from domain.repositories.repository_factory_interface import IRepositoryFactory
from domain.services.document_cleaner_interface import IDocumentCleaner
from domain.services.logger_interface import ILogger


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

        cleaning_result = self.document_cleaner.clean(raw_documents)
        cleaned_entities = cleaning_result.entities
        cleaning_errors = cleaning_result.cleaning_errors

        self.logger.info(
            f"Cleaned {len(cleaned_entities)} entities from "
            f"{len(raw_documents)} raw documents"
        )

        repository = self.repository_factory.get_repository(input_data)
        save_result = (
            repository.upsert_batch(cast(List, cleaned_entities))
            if cleaned_entities
            else {"created": 0, "updated": 0, "errors": []}
        )
        self.logger.info(f"Saved entities: {save_result}")

        # Calculate errors differently for OFFERS vs CORPS/CONCOURS
        if input_data == DocumentType.OFFERS:
            # For OFFERS: use cleaning_errors from cleaner + save errors
            all_errors = cleaning_errors + cast(
                List[Dict[str, str]], save_result["errors"]
            )
            total_errors = len(all_errors)
        else:
            # For CORPS/CONCOURS: filtered documents = errors
            cleaning_error_count = len(raw_documents) - len(cleaned_entities)
            save_errors = len(save_result["errors"])
            total_errors = cleaning_error_count + save_errors
            all_errors = cast(List[Dict[str, str]], save_result["errors"])

        return {
            "processed": len(raw_documents),
            "cleaned": len(cleaned_entities),
            "created": save_result["created"],
            "updated": save_result["updated"],
            "errors": total_errors,
            "error_details": all_errors,
        }
