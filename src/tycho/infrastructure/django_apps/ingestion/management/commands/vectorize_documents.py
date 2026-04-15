from django.core.management.base import BaseCommand

from domain.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from infrastructure.django_apps.ingestion.tasks import vectorize_documents


class Command(BaseCommand):
    help = "Vectorize documents by type"

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

    def handle(self, *args, **options):
        document_type = DocumentType(options["type"])

        self.logger.info(
            "Enqueuing vectorization task for %s...",
            document_type.value,
        )
        vectorize_documents(document_type)
        self.logger.info(self.style.SUCCESS("✅ Task enqueued successfully."))
