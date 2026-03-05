from django.core.management.base import BaseCommand, CommandError

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container


class Command(BaseCommand):
    help = "Load documents by type (CORPS, CONCOURS, etc.)"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()

    def add_arguments(self, parser):
        parser.add_argument(
            "--type",
            required=True,
            choices=[DocumentType.CORPS.value, DocumentType.OFFERS.value],
            help="Type of documents to load",
        )

    def handle(self, *args, **options):
        try:
            document_type = DocumentType(options["type"])
            load_documents_usecase = self.container.load_documents_usecase()
            archive_offers_usecase = self.container.archive_offers_usecase()

            self.logger.info("Loading documents of type: %s", document_type.value)

            input_data = LoadDocumentsInput(
                operation_type=LoadOperationType.FETCH_FROM_API,
                kwargs={"document_type": document_type},
            )
            result = load_documents_usecase.execute(input_data)

            self.logger.info(
                "✅ Load completed: %s created, %s updated",
                result["created"],
                result["updated"],
            )

            if result["errors"]:
                self.logger.warning("⚠️ %d errors occurred", len(result["errors"]))

            if document_type == DocumentType.OFFERS and result["external_ids"]:
                archived_offers_count = archive_offers_usecase.execute(
                    result["external_ids"]
                )
                self.logger.info(
                    "✅ Archiving completed: %d offers archived", archived_offers_count
                )

        except Exception as e:
            raise CommandError(f"Failed to load documents: {str(e)}") from e
