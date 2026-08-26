from datetime import date
from typing import Iterator

import httpx
from pydantic import HttpUrl
from pydantic.dataclasses import dataclass

from domain.gateways.organisme_gateway import IOrganismeGateway
from domain.value_objects.organisme import OrganismeData, OrganismeImportResource
from infrastructure.exceptions.exceptions import ExternalApiError

REFERENTIEL_GIPCDG = "GIPCDG"
API_STATUS_OK = 200


@dataclass(frozen=True)
class GipcdgConfig:
    api_key: str
    collectivites_api_url: HttpUrl


class GipcdgOrganismeGateway(IOrganismeGateway):
    def __init__(self, api_key: str, collectivites_api_url: str, timeout: int = 30):
        config = GipcdgConfig(
            api_key=api_key, collectivites_api_url=HttpUrl(collectivites_api_url)
        )
        self.api_key = config.api_key
        self.collectivites_api_url = str(config.collectivites_api_url)
        self.timeout = timeout

    def find_resource(self) -> OrganismeImportResource:
        return OrganismeImportResource(
            url=self.collectivites_api_url, millesime=date.today()
        )

    def stream_organismes(
        self, resource: OrganismeImportResource
    ) -> Iterator[OrganismeData]:
        offset = 0
        while True:
            collectivites = self._fetch_page(resource.url, offset)
            if not collectivites:
                return

            for collectivite in collectivites:
                external_id = collectivite.get("id_col")
                if external_id is None:
                    continue
                yield OrganismeData(
                    referentiel=REFERENTIEL_GIPCDG,
                    external_id=str(external_id),
                    data=collectivite,
                )

            last_rank = collectivites[-1].get("_rank")
            total = collectivites[-1].get("_total")
            if last_rank is None or total is None or last_rank >= total:
                return

            offset += len(collectivites)

    def _fetch_page(self, url: str, offset: int) -> list[dict]:
        request_url = httpx.URL(url).copy_merge_params({"offset": offset})
        try:
            response = httpx.get(
                request_url,
                headers={"X-API-Key": self.api_key, "Accept": "application/json"},
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as err:
            raise ExternalApiError(
                "Erreur lors de la récupération des collectivités GIPCDG",
                details={"url": str(request_url), "error": str(err)},
            ) from err

        payload = response.json()
        if payload.get("status") != API_STATUS_OK:
            raise ExternalApiError(
                "Réponse invalide de l'API GIPCDG",
                details={"url": str(request_url), "status": payload.get("status")},
            )

        return payload.get("success") or []
