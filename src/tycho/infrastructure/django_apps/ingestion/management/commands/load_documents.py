"""Django management command to load documents by type."""

import logging

from django.core.management.base import BaseCommand, CommandError

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container

OPERATION_TYPE_MAPPING = {
    DocumentType.OFFERS: LoadOperationType.FETCH_FROM_TALENTSOFT_FRONT_API,
    DocumentType.CORPS: LoadOperationType.FETCH_FROM_INGRES_API,
}


class Command(BaseCommand):
    """Load documents by type using LoadDocumentsUsecase."""

    help = "Load documents by type (CORPS, CONCOURS, etc.)"

    def __init__(self, *args, **kwargs):
        """Initialize the command with logger."""
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

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
            container = create_ingestion_container()
            usecase = container.load_documents_usecase()

            self.logger.info(f"Loading documents of type: {document_type.value}")

            # Map document types to their appropriate operation types

            operation_type = OPERATION_TYPE_MAPPING.get(document_type, None)
            if not operation_type:
                raise CommandError(f"Unsupported document type: {document_type}")

            input_data = LoadDocumentsInput(
                operation_type=operation_type,
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
