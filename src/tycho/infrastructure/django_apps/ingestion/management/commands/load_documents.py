"""Django management command to load documents by type."""

from django.core.management.base import BaseCommand, CommandError

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container


class Command(BaseCommand):
    """Load documents by type using LoadDocumentsUsecase."""

    help = "Load documents by type (CORPS, CONCOURS, etc.)"

    def __init__(self, *args, **kwargs):
        """Initialize the command with logger."""
        super().__init__(*args, **kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--type",
            required=True,
            choices=[DocumentType.CORPS.value, DocumentType.OFFERS.value],
            help="Type of documents to load",
        )

    def handle(self, *args, **options):
        """Execute the command."""
        try:
            document_type = DocumentType(options["type"])
            usecase = self.container.load_documents_usecase()

            self.logger.info(f"Loading documents of type: {document_type.value}")

            input_data = LoadDocumentsInput(
                operation_type=LoadOperationType.FETCH_FROM_API,
                kwargs={"document_type": document_type},
            )
            result = usecase.execute(input_data)

            self.logger.info(
                f"✅ Load completed: {result['created']} created, "
                f"{result['updated']} updated"
            )

            if result["errors"]:
                self.logger.warning(f"⚠️  {len(result['errors'])} errors occurred")

        except Exception as e:
            raise CommandError(f"Failed to load documents: {str(e)}") from e
