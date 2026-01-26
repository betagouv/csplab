"""LoadDocuments usecase."""

from typing import cast

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from domain.entities.document import DocumentType
from domain.interfaces.usecase_interface import IUseCase
from domain.repositories.document_repository_interface import (
    IDocumentRepository,
    IUpsertResult,
)
from domain.services.logger_interface import ILogger
from infrastructure.gateways.ingestion import load_documents_strategy_factory


class LoadDocumentsUsecase(IUseCase[LoadDocumentsInput, IUpsertResult]):
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
        documents, has_more = strategy.load_documents(**input_data.kwargs)

        document_type = cast(DocumentType, input_data.kwargs.get("document_type"))

        result = self.document_repository.upsert_batch(documents, document_type)
        return result
