from typing import Protocol

from referentiel.entities.api_log import ApiLog


class IApiLogRepository(Protocol):
    def save(self, api_log: ApiLog) -> None: ...
