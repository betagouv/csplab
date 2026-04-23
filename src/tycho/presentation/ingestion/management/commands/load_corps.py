from django.core.management.base import BaseCommand

from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from infrastructure.django_apps.ingestion.tasks import load_corps


class Command(BaseCommand):
    help = "Load documents, type CORPS"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()

    def handle(self, *args, **options):
        self.logger.info("Enqueuing load task for CORPS...")
        load_corps()
        self.logger.info(self.style.SUCCESS("✅ Task enqueued successfully."))
