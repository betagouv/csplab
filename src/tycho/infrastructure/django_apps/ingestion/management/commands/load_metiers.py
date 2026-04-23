from django.core.management.base import BaseCommand

from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from infrastructure.django_apps.ingestion.tasks import load_metiers


class Command(BaseCommand):
    help = "Load documents, type METIERS"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()

    def handle(self, *args, **options):
        self.logger.info("Enqueuing load task for METIERS...")
        load_metiers()
        self.logger.info("✅ Task enqueued successfully.")
