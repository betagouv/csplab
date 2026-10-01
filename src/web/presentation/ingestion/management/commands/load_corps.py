from django.core.management.base import BaseCommand

from domain.ingestion.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from presentation.ingestion.tasks import enqueue_ingestion_from_api


class Command(BaseCommand):
    help = "Load, clean and vectorize documents, type CORPS"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()

    def handle(self, *args, **options):
        self.logger.info("Enqueuing load, clean and vectorize tasks for CORPS...")
        enqueue_ingestion_from_api(DocumentType.CORPS)
        self.logger.info("✅ Tasks enqueued successfully.")
