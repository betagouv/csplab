from referentiel.entities.api_log import ApiLog
from referentiel.repositories.api_log_repository_interface import IApiLogRepository

from infrastructure.django_apps.ingestion.models.api_log import ApiLogModel


class PostgresApiLogRepository(IApiLogRepository):
    def save(self, api_log: ApiLog) -> None:
        ApiLogModel.from_entity(api_log).save()
