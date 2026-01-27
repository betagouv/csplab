"""CleanDocuments usecase."""

from typing import Any, Dict, List, cast

from domain.entities.concours import Concours
from domain.entities.corps import Corps
from domain.entities.document import DocumentType
from domain.entities.offer import Offer
from domain.exceptions.document_error import InvalidDocumentTypeError
from domain.interfaces.entity_interface import IEntity
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.repositories.corps_repository_interface import ICorpsRepository
from domain.repositories.document_repository_interface import IDocumentRepository
from domain.repositories.offers_repository_interface import IOffersRepository
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

        if input_data == DocumentType.CORPS:
            corps_repository = cast(
                ICorpsRepository, self.repository_factory.get_repository(input_data)
            )
            save_result = corps_repository.upsert_batch(
                cast(List[Corps], cleaned_entities)
            )
        elif input_data == DocumentType.CONCOURS:
            concours_repository = cast(
                IConcoursRepository, self.repository_factory.get_repository(input_data)
            )
            save_result = concours_repository.upsert_batch(
                cast(List[Concours], cleaned_entities)
            )
        elif input_data == DocumentType.OFFERS:
            offer_repository = cast(
                IOffersRepository, self.repository_factory.get_repository(input_data)
            )
            save_result = offer_repository.upsert_batch(
                cast(List[Offer], cleaned_entities)
            )
        else:
            raise InvalidDocumentTypeError(input_data.value)

        self.logger.info(f"Saved entities: {save_result}")

        if save_result["errors"]:
            for error in save_result["errors"]:
                self.logger.error(
                    f"Failed to save entity {error['entity_id']}: {error['error']}"
                )

        # Calculate total errors: cleaning errors + save errors
        cleaning_errors = len(raw_documents) - len(cleaned_entities)
        save_errors = len(save_result["errors"])
        total_errors = cleaning_errors + save_errors

        return {
            "processed": len(raw_documents),
            "cleaned": len(cleaned_entities),
            "created": save_result["created"],
            "updated": save_result["updated"],
            "errors": total_errors,
            "error_details": save_result["errors"],
        }
