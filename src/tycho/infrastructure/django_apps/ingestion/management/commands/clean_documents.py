from django.core.management.base import BaseCommand

from domain.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from infrastructure.django_apps.ingestion.tasks import clean_documents


class Command(BaseCommand):
    help = "Clean documents by type"

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
            help="Type of documents to clean",
        )

    def handle(self, *args, **options):
        document_type = DocumentType(options["type"])

        self.logger.info(
            "Enqueuing clean task for %s...",
            document_type.value,
        )
        clean_documents(document_type)
        self.logger.info("✅ Task enqueued successfully.")
