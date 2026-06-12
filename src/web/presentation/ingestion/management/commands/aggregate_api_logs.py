from datetime import date, timedelta

from django.core.management.base import BaseCommand

from presentation.ingestion.tasks import aggregate_api_logs


class Command(BaseCommand):
    help = "Aggregate API logs by day, method, path, and token_type"

    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            type=date.fromisoformat,
            default=None,
            help="Date to aggregate (YYYY-MM-DD). Defaults to yesterday.",
        )

    def handle(self, *args, **options):
        target_date = options["date"] or date.today() - timedelta(days=1)
        aggregate_api_logs.call_local(target_date)
