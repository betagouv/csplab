"""Django management command to load documents by type."""

from django.core.management.base import BaseCommand, CommandError

from apps.ingestion.application.interfaces.load_documents_input import (
    LoadDocumentsInput,
)
from apps.ingestion.application.interfaces.load_operation_type import LoadOperationType
from apps.ingestion.container_singleton import IngestionContainerSingleton
from core.entities.document import DocumentType


class Command(BaseCommand):
    """Load documents by type using LoadDocumentsUsecase."""

    help = "Load documents by type (CORPS, CONCOURS, etc.)"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--type",
            required=True,
            choices=["CORPS"],
            help="Type of documents to load",
        )

    def handle(self, *args, **options):
        """Execute the command."""
        try:
            document_type = DocumentType(options["type"])
            container = IngestionContainerSingleton.get_container()
            usecase = container.load_documents_usecase()

            self.stdout.write(f"Loading documents of type: {document_type.value}")
            input_data = LoadDocumentsInput(
                operation_type=LoadOperationType.FETCH_FROM_API,
                kwargs={"document_type": document_type},
            )
            result = usecase.execute(input_data)

            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Load completed: {result['created']} created, "
                    f"{result['updated']} updated"
                )
            )

            if result["errors"]:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  {len(result['errors'])} errors occurred")
                )

        except Exception as e:
            raise CommandError(f"Failed to load documents: {str(e)}") from e
