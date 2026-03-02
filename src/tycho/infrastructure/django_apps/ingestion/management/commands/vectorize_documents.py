from django.core.management.base import BaseCommand, CommandError

from domain.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container


class Command(BaseCommand):
    help = "Vectorize documents by type (CORPS, CONCOURS)"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()

    def add_arguments(self, parser):
        parser.add_argument(
            "--type",
            required=True,
            choices=[
                DocumentType.CORPS.value,
                DocumentType.CONCOURS.value,
                DocumentType.OFFERS.value,
            ],
            help="Type of documents to vectorize",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=250,
            help="Limit number of documents to vectorize (optional)",
        )

    def handle(self, *args, **options):
        try:
            document_type = DocumentType(options["type"])

            usecase = self.container.vectorize_documents_usecase()
            result = usecase.execute(document_type, options["limit"])
            self.logger.info("Vectorization command completed")
            self.logger.info(
                "✅ Vectorization completed: %d of %d vectorized",
                result["vectorized"],
                result["processed"],
            )

            if result["errors"] > 0:
                self.logger.warning("⚠️ %d errors occurred", result["errors"])

            if result.get("error_details"):
                for error in result["error_details"]:
                    self.logger.warning(
                        "%s - %s: %s",
                        error["source_type"],
                        error["source_id"],
                        error["error"],
                    )
        except Exception as e:
            raise CommandError(f"Failed to vectorize documents: {str(e)}") from e
