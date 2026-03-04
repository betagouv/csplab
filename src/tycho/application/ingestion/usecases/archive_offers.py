from typing import List

from django.db import transaction

from domain.entities.document import DocumentType
from domain.interfaces.usecase_interface import IUseCase
from domain.repositories.offers_repository_interface import IOffersRepository
from domain.repositories.vector_repository_interface import IVectorRepository
from domain.services.logger_interface import ILogger


class ArchiveOffersUsecase(IUseCase[List[str], int]):
    def __init__(
        self,
        offers_repository: IOffersRepository,
        vector_repository: IVectorRepository,
        logger: ILogger,
    ):
        self.offers_repository = offers_repository
        self.vector_repository = vector_repository
        self.logger = logger

    def execute(self, external_ids: List[str]) -> int:
        self.logger.info("Archive %d offers", len(external_ids))

        to_archive_ids = self.offers_repository.find_by_missing_external_ids(
            external_ids
        )

        # unit of work required later
        with transaction.atomic():
            archived_offers_count = self.offers_repository.mark_as_archived(
                to_archive_ids
            )
            deleted_vectors_count = (
                self.vector_repository.delete_by_entity_ids_and_document_type(
                    to_archive_ids, DocumentType.OFFERS
                )
            )

            self.logger.info(
                "%d offers archived, %d vectorized offers deleted",
                archived_offers_count,
                deleted_vectors_count,
            )

        return archived_offers_count
