"""CleanDocuments usecase."""

from typing import Any, Dict, List, cast

from core.entities.concours import Concours
from core.entities.corps import Corps
from core.entities.document import DocumentType
from core.entities.offer import Offer
from core.errors.document_error import InvalidDocumentTypeError
from core.interfaces.entity_interface import IEntity
from core.repositories.concours_repository_interface import IConcoursRepository
from core.repositories.corps_repository_interface import ICorpsRepository
from core.repositories.document_repository_interface import IDocumentRepository
from core.repositories.offer_repository_interface import IOfferRepository
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
        elif input_data == DocumentType.OFFER:
            offer_repository = cast(
                IOfferRepository, self.repository_factory.get_repository(input_data)
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

        return {
            "processed": len(raw_documents),
            "cleaned": len(cleaned_entities),
            "created": save_result["created"],
            "updated": save_result["updated"],
            "errors": len(save_result["errors"]),
            "error_details": save_result["errors"],
        }
