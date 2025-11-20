"""LoadDocuments usecase."""

from apps.ingestion.containers import IngestionContainer
from core.entities.document import DocumentType
from core.interfaces.document_repository_interface import IUpsertResult


class LoadDocumentsUsecase:
    """Usecase for loading and persisting documents."""

    def __init__(self, container: IngestionContainer):
        """Initialize with container."""
        self.container = container

    def execute(self, document_type: DocumentType) -> IUpsertResult:
        """Execute the usecase to load and persist documents."""
        try:
            repository = self.container.document_repository()

            documents = repository.fetch_by_type(document_type)

            result = repository.upsert_batch(documents)

            return result

        except Exception:
            logger = self.container.logger_service().get_logger(
                "INGESTION::APPLICATION::LoadDocumentsUsecase::execute"
            )
            logger.error("Error loading documents")
            raise
