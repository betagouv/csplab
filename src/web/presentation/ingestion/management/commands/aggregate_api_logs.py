import logging
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from infrastructure.di.shared.shared_container import SharedContainer

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Aggregate API logs by day, method, path, and token_type"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        container = SharedContainer()
        self.api_log_repository = container.api_log_repository()
        self.aggregation_repository = container.api_log_daily_aggregation_repository()

    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            type=date.fromisoformat,
            default=None,
            help="Date to aggregate (YYYY-MM-DD). Defaults to yesterday.",
        )

    def handle(self, *args, **options):
        target_date = options["date"] or date.today() - timedelta(days=1)

        logger.info("Aggregating API logs for %s...", target_date)

        aggregations = self.api_log_repository.get_counts_by_date(target_date)

        if not aggregations:
            logger.info("No API logs found for %s, skipping.", target_date)
            self.stdout.write(f"No logs for {target_date}.")
            return

        self.aggregation_repository.replace_for_date(target_date, aggregations)

        logger.info(
            "Inserted %d aggregation rows for %s.", len(aggregations), target_date
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Aggregated {len(aggregations)} rows for {target_date}."
            )
        )
