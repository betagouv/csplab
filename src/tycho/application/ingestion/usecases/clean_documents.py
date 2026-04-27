from typing import Any, Dict, List, cast

from django.db import transaction

from domain.entities.document import DocumentType
from domain.interfaces.entity_interface import IEntity, IOfferEntity
from domain.interfaces.usecase_interface import IUseCase
from domain.repositories.document_repository_interface import (
    IDocumentRepository,
    IUpsertResult,
)
from domain.repositories.metier_repository_interface import IMetierRepository
from domain.repositories.repository_factory_interface import IRepositoryFactory
from domain.services.document_cleaner_interface import IDocumentCleaner
from domain.services.logger_interface import ILogger


class CleanDocumentsUsecase(IUseCase[DocumentType, Dict[str, Any]]):
    def __init__(
        self,
        document_repository: IDocumentRepository,
        document_cleaner: IDocumentCleaner[IEntity],
        repository_factory: IRepositoryFactory,
        logger: ILogger,
    ):
        self.document_repository = document_repository
        self.document_cleaner = document_cleaner
        self.repository_factory = repository_factory
        self.logger = logger

    def execute(self, document_type: DocumentType, limit: int = 1000) -> Dict[str, Any]:
        self.logger.info("Starting cleaning %d document type: %s", limit, document_type)
        results: Dict[str, Any] = {
            "processed": 0,
            "cleaned": 0,
            "created": 0,
            "updated": 0,
            "errors": 0,
            "error_details": [],
        }

        if document_type == DocumentType.OFFERS:
            return self._clean_offers(document_type, limit, results)
        return self._clean_concours_or_corps_metiers(document_type, results)

    def _clean_offers(
        self, document_type: DocumentType, limit: int, results: Dict[str, Any]
    ) -> Dict[str, Any]:
        raw_documents = self.document_repository.get_pending_processing(
            document_type=document_type,
            limit=limit,
        )

        cleaning_result = self.document_cleaner.clean(raw_documents)
        cleaned_entities = cast(List[IOfferEntity], cleaning_result.entities)
        cleaning_errors = cleaning_result.cleaning_errors

        cleaned_entities_external_id = [
            cleaned_entity.external_id for cleaned_entity in cleaned_entities
        ]

        cleaned_raw_documents = [
            raw_doc
            for raw_doc in raw_documents
            if raw_doc.external_id in cleaned_entities_external_id
        ]
        failed_raw_documents = [
            raw_doc
            for raw_doc in raw_documents
            if raw_doc.external_id not in cleaned_entities_external_id
        ]

        with transaction.atomic():
            if cleaned_entities:
                repository = self.repository_factory.get_repository(document_type)
                save_result: IUpsertResult = repository.upsert_batch(
                    cast(List, cleaned_entities)
                )
                self.document_repository.mark_as_processed(
                    cast(List, cleaned_raw_documents)
                )

                results["processed"] = len(raw_documents)  # type: ignore
                results["cleaned"] = len(cleaned_entities)  # type: ignore
                results["created"] = save_result["created"]  # type: ignore
                results["updated"] = save_result["updated"]  # type: ignore
                results["errors"] = len(cleaning_errors)  # type: ignore
                results["error_details"] = cleaning_errors  # type: ignore[operator]

            if cleaning_errors and failed_raw_documents:
                error_msg = " | ".join(
                    [str(err.get("error", "Unknown error")) for err in cleaning_errors]
                )
                self.document_repository.mark_as_failed(
                    cast(List, failed_raw_documents), error_msg
                )

        return results

    def _clean_concours_or_corps_metiers(
        self, document_type: DocumentType, results: Dict[str, Any]
    ) -> Dict[str, Any]:
        start = 0
        has_more = True

        while has_more:
            raw_documents, has_more = self.document_repository.find_by_type(
                document_type, start
            )

            repository = self.repository_factory.get_repository(document_type)

            if document_type == DocumentType.METIERS:
                metier_repository = cast(IMetierRepository, repository)
                save_result: IUpsertResult = metier_repository.upsert_batch_rich_data(
                    raw_documents
                )

                cleaned_count = save_result["created"] + save_result["updated"]

                results["processed"] += len(raw_documents)  # type: ignore
                results["cleaned"] += cleaned_count  # type: ignore
                results["created"] += save_result["created"]  # type: ignore
                results["updated"] += save_result["updated"]  # type: ignore
                results["errors"] += len(save_result["errors"])  # type: ignore
                results["error_details"] += save_result["errors"]  # type: ignore[operator]
            else:
                cleaning_result = self.document_cleaner.clean(raw_documents)
                cleaned_entities = cleaning_result.entities

                other_save_result: IUpsertResult = (
                    repository.upsert_batch(cast(List, cleaned_entities))
                    if cleaned_entities
                    else {"created": 0, "updated": 0, "errors": []}
                )

                results["processed"] += len(raw_documents)  # type: ignore
                results["cleaned"] += len(cleaned_entities)  # type: ignore
                results["created"] += other_save_result["created"]  # type: ignore
                results["updated"] += other_save_result["updated"]  # type: ignore

                cleaning_error_count = len(raw_documents) - len(cleaned_entities)
                results["errors"] += cleaning_error_count + len(
                    other_save_result["errors"]
                )  # type: ignore
                results["error_details"] += other_save_result["errors"]  # type: ignore[operator]

            start += 1

        return results
