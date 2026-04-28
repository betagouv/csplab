from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand

from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from presentation.ingestion.tasks import archive_offers

NOW = datetime.now()


class Command(BaseCommand):
    help = "Load documents, type CORPS"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()

    def add_arguments(self, parser):
        parser.add_argument(
            "--updated-after",
            type=datetime.fromisoformat,
            default=NOW - relativedelta(hours=24),
            help="ISO 8601 date to look back from, e.g. 2026-04-01T00:00:00",
        )

    def handle(self, *args, **options):
        self.logger.info("Enqueuing archive task for OFFERS...")
        updated_after = options["updated_after"]
        archive_offers(updated_after=updated_after)
        self.logger.info("✅ Task enqueued successfully.")
