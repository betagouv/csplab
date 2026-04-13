from typing import List, cast

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from domain.entities.document import DocumentType
from domain.exceptions.document_error import InvalidDocumentTypeError
from domain.gateways.document_gateway_interface import IDocumentGateway
from domain.interfaces.async_usecase_interface import IAsyncUseCase
from domain.repositories.document_repository_interface import (
    IDocumentRepository,
    IUpsertResult,
)
from domain.services.logger_interface import ILogger

MAX_ITERATIONS = 1000


class LoadOffersUsecase(IAsyncUseCase[LoadDocumentsInput, IUpsertResult]):
    def __init__(
        self,
        document_repository: IDocumentRepository,
        document_gateway: IDocumentGateway,
        logger: ILogger,
    ):
        self.document_repository = document_repository
        self.document_gateway = document_gateway
        self.logger = logger

    async def execute(self, input_data: LoadDocumentsInput) -> IUpsertResult:
        document_type = cast(DocumentType, input_data.kwargs.get("document_type"))
        reload = input_data.kwargs.get("reload", False)
        batch_size = input_data.kwargs.get("batch_size", 100)
        if document_type != DocumentType.OFFERS:
            raise InvalidDocumentTypeError(document_type.value)

        has_more = True
        page = 1
        batch_result: IUpsertResult = {"created": 0, "updated": 0, "errors": []}

        while has_more and page < MAX_ITERATIONS:
            self.logger.info("LoadOffers, fetching page %d", page)

            fetched_documents, has_more = await self.document_gateway.fetch_by_type(
                document_type=document_type, start=page, batch_size=batch_size
            )
            if not fetched_documents:
                break

            existing_documents = self.document_repository.find_by_external_ids(
                document_type=document_type, documents=cast(List, fetched_documents)
            )

            documents = self.document_repository.get_documents_to_upsert(
                document_type=document_type,
                fetched_documents=cast(List, fetched_documents),
                existing_documents=cast(List, existing_documents),
            )
            if bool(documents):
                self.logger.info(
                    "LoadOffers, page %d, found %d offers to upsert",
                    page,
                    len(documents),
                )
            elif not reload:
                self.logger.info(
                    "LoadOffers, page %d, everything seems to be up-to-date… "
                    "STOPPING iterations",
                    page,
                )
                break
            else:
                self.logger.info(
                    "LoadOffers, page %d, everything seems to be up-to-date… "
                    "CONTINUING (reload=True)",
                    page,
                )

            detail_documents = []
            for document in documents:
                if document.external_id is not None:
                    detail = await self.document_gateway.get_detail(
                        document_type=document_type, external_id=document.external_id
                    )
                    detail_documents.append(detail)

            result = self.document_repository.upsert_batch(
                detail_documents, document_type
            )
            self.logger.info(
                "LoadOffers, page %d, upsert: %d created, %d updated",
                page,
                result["created"],
                result["updated"],
            )

            batch_result["created"] += result["created"]
            batch_result["updated"] += result["updated"]
            batch_result["errors"].extend(result["errors"])

            if has_more:
                page += 1

        return batch_result
