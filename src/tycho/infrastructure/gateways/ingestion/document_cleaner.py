"""Document cleaner factory."""

from typing import List

from domain.entities.document import Document, DocumentType
from domain.exceptions.document_error import (
    MixedDocumentTypesError,
    UnsupportedDocumentTypeError,
)
from domain.interfaces.entity_interface import IEntity
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.repositories.corps_repository_interface import ICorpsRepository
from domain.services.document_cleaner_interface import CleaningResult, IDocumentCleaner
from domain.services.logger_interface import ILogger
from infrastructure.gateways.ingestion.concours_cleaner import ConcoursCleaner
from infrastructure.gateways.ingestion.corps_cleaner import CorpsCleaner
from infrastructure.gateways.ingestion.offers_cleaner import OffersCleaner


class DocumentCleaner(IDocumentCleaner[IEntity]):
    """Factory for creating appropriate document cleaners based on document type.

    Implements IDocumentCleaner[IEntity] protocol.
    """

    def __init__(
        self,
        logger: ILogger,
        corps_repository: ICorpsRepository,
        concours_repository: IConcoursRepository,
    ):
        """Initialize the factory with available cleaners."""
        self._cleaners = {
            DocumentType.CORPS: CorpsCleaner(logger, corps_repository),
            DocumentType.CONCOURS: ConcoursCleaner(logger, concours_repository),
            DocumentType.OFFERS: OffersCleaner(logger),
        }

    def clean(self, raw_documents: List[Document]) -> CleaningResult[IEntity]:
        """Clean documents using the appropriate cleaner based on document type."""
        if not raw_documents:
            return CleaningResult(entities=[], cleaning_errors=[])

        document_types = {doc.type for doc in raw_documents}
        if len(document_types) > 1:
            raise MixedDocumentTypesError(document_types)

        document_type = next(iter(document_types))

        # Get the appropriate cleaner
        if document_type not in self._cleaners:
            raise UnsupportedDocumentTypeError(document_type.value)

        cleaner = self._cleaners[document_type]
        return cleaner.clean(raw_documents)
