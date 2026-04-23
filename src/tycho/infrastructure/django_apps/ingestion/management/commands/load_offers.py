from django.core.management.base import BaseCommand

from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from infrastructure.django_apps.ingestion.tasks import load_offers


class Command(BaseCommand):
    help = "Load documents, type OFFERS"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()

    def add_arguments(self, parser):
        parser.add_argument(
            "--reload",
            action="store_true",
            default=False,
            help="Browse all offers even if a batch find nothing to upsert",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=100,
            help="Number of offers to fetch per batch (default: 100)",
        )

    def handle(self, *args, **options):
        reload = options["reload"]
        batch_size = options["batch_size"]

        self.logger.info("Enqueuing load task for OFFERS...")
        load_offers(reload=reload, batch_size=batch_size)
        self.logger.info("✅ Task enqueued successfully.")
