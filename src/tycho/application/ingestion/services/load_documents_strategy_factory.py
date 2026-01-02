"""Load documents strategy factory."""

from typing import Union

from application.ingestion.interfaces.load_operation_type import LoadOperationType
from application.ingestion.services.load_documents_strategies import (
    FetchFromApiStrategy,
    UploadFromCsvStrategy,
)
from apps.ingestion.exceptions import InvalidLoadOperationError
from domain.repositories.document_repository_interface import IDocumentFetcher


class LoadDocumentsStrategyFactory:
    """Factory for creating load documents strategies."""

    def __init__(self, document_fetcher: IDocumentFetcher):
        """Initialize with dependencies."""
        self.document_fetcher = document_fetcher

    def create(
        self, operation_type: LoadOperationType
    ) -> Union[FetchFromApiStrategy, UploadFromCsvStrategy]:
        """Create strategy based on operation type."""
        match operation_type:
            case LoadOperationType.FETCH_FROM_API:
                return FetchFromApiStrategy(self.document_fetcher)
            case LoadOperationType.UPLOAD_FROM_CSV:
                return UploadFromCsvStrategy()
            case _:
                raise InvalidLoadOperationError(str(operation_type))
