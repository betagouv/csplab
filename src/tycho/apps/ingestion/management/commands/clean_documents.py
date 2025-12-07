"""Django management command to clean documents by type."""

from django.core.management.base import BaseCommand, CommandError

from apps.ingestion.container_singleton import IngestionContainerSingleton
from core.entities.document import DocumentType


class Command(BaseCommand):
    """Clean documents by type using CleanDocumentsUsecase."""

    help = "Clean documents by type (CORPS, CONCOURS, etc.)"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--type",
            required=True,
            choices=["CORPS"],
            help="Type of documents to clean",
        )

    def handle(self, *args, **options):
        """Execute the command."""
        try:
            document_type = DocumentType(options["type"])
            container = IngestionContainerSingleton.get_container()
            usecase = container.clean_documents_usecase()
            self.stdout.write(f"Cleaning documents of type: {document_type.value}")
            result = usecase.execute(document_type)
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Clean completed: {result['cleaned']}/{result['processed']}"
                    "documents cleaned"
                )
            )

            if result["errors"] > 0:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  {result['errors']} errors occurred")
                )

            # Display error details if any
            if result.get("error_details"):
                self.stdout.write("Error details:")
                for error in result["error_details"]:
                    self.stdout.write(
                        f"  - Entity {error['entity_id']}: {error['error']}"
                    )

        except Exception as e:
            raise CommandError(f"Failed to clean documents: {str(e)}") from e
