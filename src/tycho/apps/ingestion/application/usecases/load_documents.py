"""LoadDocuments usecase."""

from core.entities.document import DocumentType
from core.repositories.document_repository_interface import (
    IDocumentRepository,
    IUpsertResult,
)
from core.services.logger_interface import ILogger


class LoadDocumentsUsecase:
    """Usecase for loading and persisting documents."""

    def __init__(self, document_repository: IDocumentRepository, logger: ILogger):
        """Initialize with dependencies."""
        self.document_repository = document_repository
        self.logger = logger.get_logger(
            "INGESTION::APPLICATION::LoadDocumentsUsecase::execute"
        )

    def execute(self, input_data: DocumentType) -> IUpsertResult:
        """Execute the usecase to load and persist documents."""
        documents = self.document_repository.fetch_by_type(input_data)
        result = self.document_repository.upsert_batch(documents)
        return result
