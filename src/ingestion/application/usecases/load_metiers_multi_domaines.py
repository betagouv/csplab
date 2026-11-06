from application.usecases._fetch_with_retry import fetch_with_retry
from infrastructure.external_gateways.web_metiers_gateway import WebMetiersGateway


class LoadMetiersMultiDomainesUsecase:
    def __init__(
        self, metiers_gateway: WebMetiersGateway, metiers_multi_domaines: set[str]
    ) -> None:
        self._metiers_gateway = metiers_gateway
        self._metiers_multi_domaines = metiers_multi_domaines

    async def execute(self) -> None:
        codes = await fetch_with_retry(
            self._metiers_gateway.fetch_metiers_multi_domaines, label="metiers"
        )
        self._metiers_multi_domaines.update(codes)
