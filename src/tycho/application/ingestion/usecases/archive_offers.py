from datetime import datetime

from asgiref.sync import async_to_sync

from domain.gateways.document_gateway_interface import IDocumentGateway
from domain.interfaces.usecase_interface import IUseCase
from domain.repositories.offers_repository_interface import (
    IArchiveResult,
    IOffersRepository,
)
from domain.repositories.vector_repository_interface import IVectorRepository
from domain.services.logger_interface import ILogger

MAX_OFFSET = 100000


class ArchiveOffersUsecase(IUseCase[datetime, IArchiveResult]):
    def __init__(
        self,
        offers_repository: IOffersRepository,
        document_gateway: IDocumentGateway,
        vector_repository: IVectorRepository,
        logger: ILogger,
    ):
        self.offers_repository = offers_repository
        self.document_gateway = document_gateway
        self.vector_repository = vector_repository
        self.logger = logger

    def execute(
        self,
        updated_after: datetime,
    ) -> IArchiveResult:
        self.logger.info(
            "Starting archiving document type: OFFERS, updated after %s",
            updated_after.strftime("%Y-%m-%d %H:%M:%S"),
        )

        batch_result: IArchiveResult = {
            "fetched": 0,
            "vector_deleted": 0,
            "entity_archived": 0,
            "errors": [],
        }

        fetched_external_ids = async_to_sync(
            self.document_gateway.get_archived_documents_by_period
        )(updated_after=updated_after)

        if not fetched_external_ids:
            return batch_result

        existing_documents = self.offers_repository.get_by_external_ids(
            fetched_external_ids
        )
        existing_document_uuids = [
            doc.id for doc in existing_documents if doc.archived_at is None
        ]
        if not existing_document_uuids:
            return batch_result

        # we do not use atomic transaction, Offers are marked as archived
        # only if each previous steps succeed, otherwise, usecase can be
        # relaunched safely on the same period

        # TODO : pass failing entity_id into response to exclude them
        # from being marked as archived
        vector_result = self.vector_repository.delete_vectorized_documents(
            existing_document_uuids
        )

        archived_count = self.offers_repository.mark_as_archived(existing_documents)

        batch_result["fetched"] = len(fetched_external_ids)
        batch_result["entity_archived"] = archived_count
        batch_result["vector_deleted"] = vector_result["deleted"]
        batch_result["errors"] = vector_result["errors"]

        return batch_result
