"""CleanDocuments usecase."""

from typing import Any, Dict, List, cast

from domain.entities.document import DocumentType
from domain.interfaces.entity_interface import IEntity
from domain.repositories.document_repository_interface import (
    IDocumentRepository,
    IUpsertResult,
)
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
        self.logger = logger

    def execute(self, input_data: DocumentType) -> Dict[str, Any]:
        """Execute the usecase to clean documents and return processing results."""
        start = 0
        has_more = True
        results = {
            "processed": 0,
            "cleaned": 0,
            "created": 0,
            "updated": 0,
            "errors": 0,
            "error_details": [],
        }

        while has_more:
            raw_documents, has_more = self.document_repository.find_by_type(
                input_data, start
            )
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
            save_result: IUpsertResult = (
                repository.upsert_batch(cast(List, cleaned_entities))
                if cleaned_entities
                else {"created": 0, "updated": 0, "errors": []}
            )
            self.logger.info(f"Saved entities: {save_result}")

            results["processed"] += len(raw_documents)  # type: ignore
            results["cleaned"] += len(cleaned_entities)  # type: ignore
            results["created"] += save_result["created"]  # type: ignore
            results["updated"] += save_result["updated"]  # type: ignore

            if input_data == DocumentType.OFFERS:
                all_errors = cleaning_errors + cast(
                    List[Dict[str, str]], save_result["errors"]
                )  # type: ignore
                results["errors"] += len(all_errors)  # type: ignore
                results["error_details"] += all_errors  # type: ignore[operator]
            else:
                cleaning_error_count = len(raw_documents) - len(cleaned_entities)
                results["errors"] += cleaning_error_count + len(save_result["errors"])  # type: ignore
                results["error_details"] += save_result["errors"]  # type: ignore[operator]

            start += 1

        return results
