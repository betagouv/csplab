from django.core.management.base import BaseCommand, CommandError

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container


class Command(BaseCommand):
    help = "Load documents, type OFFERS"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()

    def add_arguments(self, parser):
        parser.add_argument(
            "--reload",
            action="store_true",
            default=False,
            help="Browse all offers even if a batch find nothing to upsert",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=100,
            help="Number of offers to fetch per batch (default: 100)",
        )

    def handle(self, *args, **options):
        reload = options["reload"]
        batch_size = options["batch_size"]
        try:
            document_type = DocumentType.OFFERS
            usecase = self.container.load_offers_usecase()

            self.logger.info("Loading documents of type: %s", document_type.value)

            input_data = LoadDocumentsInput(
                operation_type=LoadOperationType.FETCH_FROM_API,
                kwargs={
                    "document_type": document_type,
                    "reload": reload,
                    "batch_size": batch_size,
                },
            )
            result = usecase.execute(input_data)

            self.logger.info(
                "✅ Load completed: %d created, %d updated",
                result["created"],
                result["updated"],
            )

            if result["errors"]:
                self.logger.warning("⚠️ %d errors occurred", len(result["errors"]))

        except Exception as e:
            raise CommandError(f"Failed to load documents: {str(e)}") from e
