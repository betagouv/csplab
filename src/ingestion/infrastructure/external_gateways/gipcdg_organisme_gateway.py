from datetime import date
from typing import Iterator

import httpx

from domain.gateways.organisme_gateway import IOrganismeGateway
from domain.value_objects.organisme import OrganismeData, OrganismeImportResource
from infrastructure.exceptions.exceptions import ExternalApiError

# https://emploi-territorial.fr/api
COLLECTIVITES_API_URL = (
    "https://emploi-territorial.fr/api/cdg/collectivites?etab=5&limit=1000"
)
REFERENTIEL_GIPCDG = "GIPCDG"
API_STATUS_OK = 200


class GipcdgOrganismeGateway(IOrganismeGateway):
    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout

    def find_resource(self) -> OrganismeImportResource:
        return OrganismeImportResource(
            url=COLLECTIVITES_API_URL, millesime=date.today()
        )

    def stream_organismes(
        self, resource: OrganismeImportResource
    ) -> Iterator[OrganismeData]:
        try:
            response = httpx.get(
                resource.url,
                headers={"X-API-Key": self.api_key, "Accept": "application/json"},
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as err:
            raise ExternalApiError(
                "Erreur lors de la récupération des collectivités GIPCDG",
                details={"url": resource.url, "error": str(err)},
            ) from err

        payload = response.json()
        if payload.get("status") != API_STATUS_OK:
            raise ExternalApiError(
                "Réponse invalide de l'API GIPCDG",
                details={"url": resource.url, "status": payload.get("status")},
            )

        for collectivite in payload.get("success") or []:
            external_id = collectivite.get("id_col")
            if external_id is None:
                continue
            yield OrganismeData(
                referentiel=REFERENTIEL_GIPCDG,
                external_id=str(external_id),
                data=collectivite,
            )
