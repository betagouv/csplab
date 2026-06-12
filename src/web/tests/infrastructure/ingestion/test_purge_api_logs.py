from datetime import date, timedelta

from infrastructure.django_apps.ingestion.models.api_log import ApiLogModel
from presentation.ingestion.tasks import purge_api_logs
from tests.factories.datetime_utils import date_to_aware_datetime
from tests.factories.ingestion.api_log_model_factory import ApiLogModelFactory

DEFAULT_DELAY = 90
OLD_DATE = date.today() - timedelta(days=DEFAULT_DELAY + 1)
RECENT_DATE = date.today() - timedelta(days=DEFAULT_DELAY - 1)
CUTOFF_DATE = date.today() - timedelta(days=DEFAULT_DELAY)


class TestPurgeApiLogsTask:
    def test_deletes_logs_older_than_retention(self, db):
        ApiLogModelFactory.create_model(timestamp=date_to_aware_datetime(OLD_DATE))

        purge_api_logs.call_local()

        assert ApiLogModel.objects.count() == 0

    def test_keeps_logs_within_retention(self, db):
        ApiLogModelFactory.create_model(timestamp=date_to_aware_datetime(RECENT_DATE))

        purge_api_logs.call_local()

        assert ApiLogModel.objects.count() == 1

    def test_keeps_logs_on_cutoff_date(self, db):
        ApiLogModelFactory.create_model(timestamp=date_to_aware_datetime(CUTOFF_DATE))

        purge_api_logs.call_local()

        assert ApiLogModel.objects.count() == 1

    def test_deletes_only_old_logs(self, db):
        ApiLogModelFactory.create_model(timestamp=date_to_aware_datetime(OLD_DATE))
        ApiLogModelFactory.create_model(timestamp=date_to_aware_datetime(RECENT_DATE))

        purge_api_logs.call_local()

        assert ApiLogModel.objects.count() == 1
        assert ApiLogModel.objects.filter(timestamp__date=RECENT_DATE).exists()

    def test_custom_retention_days(self, db):
        ApiLogModelFactory.create_model(timestamp=date_to_aware_datetime(RECENT_DATE))

        purge_api_logs.call_local(retention_days=10)

        assert ApiLogModel.objects.count() == 0

    def test_no_logs_does_not_raise(self, db):
        purge_api_logs.call_local()
