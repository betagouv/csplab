from django.core.management.base import BaseCommand, CommandError

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container


class Command(BaseCommand):
    help = "Load documents, type CORPS"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()

    def handle(self, *args, **options):
        try:
            document_type = DocumentType.CORPS
            usecase = self.container.load_documents_usecase()

            self.logger.info("Loading documents of type: %s", document_type.value)

            input_data = LoadDocumentsInput(
                operation_type=LoadOperationType.FETCH_FROM_API,
                kwargs={"document_type": document_type},
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
