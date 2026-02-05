"""Django management command to vectorize documents by type."""

from django.core.management.base import BaseCommand, CommandError

from domain.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container


class Command(BaseCommand):
    """Vectorize documents by type using VectorizeDocumentsUsecase."""

    help = "Vectorize documents by type (CORPS, CONCOURS)"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--type",
            required=True,
            choices=["CORPS", "CONCOURS"],
            help="Type of documents to vectorize",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Limit number of documents to vectorize (optional)",
        )

    def handle(self, *args, **options):
        """Execute the command."""
        try:
            document_type = DocumentType(options["type"])
            container = create_ingestion_container()

            repository_factory = container.repository_factory()
            repository = repository_factory.get_repository(document_type)
            usecase = container.vectorize_documents_usecase()

            # Get entities to vectorize based on type
            limit = options.get("limit")
            if limit:
                self.stdout.write(
                    f"Fetching {limit} entities of type: {document_type.value}"
                )
            else:
                self.stdout.write(
                    f"Fetching all entities of type: {document_type.value}"
                )

            entities = repository.get_all()
            if entities and limit:
                entities = entities[:limit]

            if not entities:
                self.stdout.write(
                    self.style.WARNING(
                        f"No entities found for type: {document_type.value}"
                    )
                )
                return

            self.stdout.write(f"Vectorizing {len(entities)} entities...")
            result = usecase.execute(entities)

            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Completed: {result['vectorized']}/{result['processed']}"
                    " documents vectorized"
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
                        f"  - {error['source_type']} {error['source_id']}:"
                        f"{error['error']}"
                    )

        except Exception as e:
            raise CommandError(f"Failed to vectorize documents: {str(e)}") from e
