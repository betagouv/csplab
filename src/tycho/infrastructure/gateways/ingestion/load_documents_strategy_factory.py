"""Load documents strategy factory."""

from typing import List, Optional, Union

from domain.entities.document import Document, DocumentType
from domain.repositories.document_repository_interface import IDocumentFetcher
from infrastructure.exceptions.ingestion_exceptions import InvalidLoadOperationError
from infrastructure.gateways.ingestion.load_documents_strategies import (
    FetchFromApiStrategy,
    UploadFromCsvStrategy,
)


class LoadDocumentsStrategyFactory:
    """Factory for creating load documents strategies."""

    def __init__(self, document_fetcher: IDocumentFetcher):
        """Initialize with dependencies."""
        self.document_fetcher = document_fetcher

    def create(
        self, document_type: DocumentType, documents: Optional[List[Document]] = None
    ) -> Union[FetchFromApiStrategy, UploadFromCsvStrategy]:
        """Create strategy based on document type."""
        match document_type:
            case DocumentType.CONCOURS:
                return UploadFromCsvStrategy(documents)
            case DocumentType.CORPS | DocumentType.GRADE | DocumentType.OFFERS:
                return FetchFromApiStrategy(self.document_fetcher)
            case _:
                raise InvalidLoadOperationError(
                    f"Unsupported document type: {document_type}"
                )
