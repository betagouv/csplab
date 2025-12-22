"""Document cleaner factory."""

from typing import List, Sequence

from apps.ingestion.infrastructure.adapters.services.concours_cleaner import (
    ConcoursCleaner,
)
from apps.ingestion.infrastructure.adapters.services.corps_cleaner import CorpsCleaner
from core.entities.document import Document, DocumentType
from core.errors.document_error import (
    MixedDocumentTypesError,
    UnsupportedDocumentTypeError,
)
from core.interfaces.entity_interface import IEntity
from core.services.document_cleaner_interface import IDocumentCleaner
from core.services.logger_interface import ILogger


class DocumentCleaner(IDocumentCleaner[IEntity]):
    """Factory for creating appropriate document cleaners based on document type.

    Implements IDocumentCleaner[IEntity] protocol.
    """

    def __init__(self, logger: ILogger):
        """Initialize the factory with available cleaners."""
        self._cleaners = {
            DocumentType.CORPS: CorpsCleaner(logger),
            DocumentType.CONCOURS: ConcoursCleaner(logger),
        }

    def clean(self, raw_documents: List[Document]) -> Sequence[IEntity]:
        """Clean documents using the appropriate cleaner based on document type."""
        if not raw_documents:
            return []

        document_types = {doc.type for doc in raw_documents}
        if len(document_types) > 1:
            raise MixedDocumentTypesError(document_types)

        document_type = next(iter(document_types))

        # Get the appropriate cleaner
        if document_type not in self._cleaners:
            raise UnsupportedDocumentTypeError(document_type.value)

        cleaner = self._cleaners[document_type]
        return cleaner.clean(raw_documents)
