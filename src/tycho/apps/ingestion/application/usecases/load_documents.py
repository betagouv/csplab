"""LoadDocuments usecase."""

from apps.ingestion.application.interfaces.load_documents_input import (
    LoadDocumentsInput,
)
from apps.ingestion.infrastructure.adapters.services import (
    load_documents_strategy_factory,
)
from core.repositories.document_repository_interface import (
    IDocumentRepository,
    IUpsertResult,
)
from core.services.logger_interface import ILogger


class LoadDocumentsUsecase:
    """Usecase for loading and persisting documents."""

    def __init__(
        self,
        strategy_factory: load_documents_strategy_factory.LoadDocumentsStrategyFactory,
        document_repository: IDocumentRepository,
        logger: ILogger,
    ):
        """Initialize with dependencies."""
        self.strategy_factory = strategy_factory
        self.document_repository = document_repository
        self.logger = logger.get_logger(
            "INGESTION::APPLICATION::LoadDocumentsUsecase::execute"
        )

    def execute(self, input_data: LoadDocumentsInput) -> IUpsertResult:
        """Execute the usecase to load and persist documents."""
        strategy = self.strategy_factory.create(input_data.operation_type)
        documents = strategy.load_documents(**input_data.kwargs)
        result = self.document_repository.upsert_batch(documents)
        return result
