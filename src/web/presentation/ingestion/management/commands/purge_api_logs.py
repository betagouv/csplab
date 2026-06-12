from django.core.management.base import BaseCommand, CommandError

from presentation.ingestion.tasks import API_LOG_MIN_RETENTION_DAYS, purge_api_logs


class Command(BaseCommand):
    help = "Purge API logs older than a retention period"

    def add_arguments(self, parser):
        parser.add_argument(
            "--retention-days",
            type=int,
            default=API_LOG_MIN_RETENTION_DAYS,
            help=(
                f"Number of days to retain API logs "
                f"(default: {API_LOG_MIN_RETENTION_DAYS})."
            ),
        )

    def handle(self, *args, **options):
        retention_days = options["retention_days"]
        if retention_days < API_LOG_MIN_RETENTION_DAYS:
            raise CommandError(
                f"--retention-days must be >= {API_LOG_MIN_RETENTION_DAYS}."
            )
        purge_api_logs.call_local(retention_days)
