import csv
import io
import json
from datetime import date
from typing import Iterator

import httpx

from domain.gateways.organisme_gateway import IOrganismeGateway
from domain.value_objects.organisme import OrganismeData, OrganismeImportResource
from domain.value_objects.organisme_referentiel import OrganismeReferentiel
from infrastructure.exceptions.exceptions import ExternalApiError

# https://api-lannuaire.service-public.fr/api/explore/v2.1/console
DILA_EXPORT_URL = (
    "https://api-lannuaire.service-public.fr/api/explore/v2.1/catalog/datasets/"
    "api-lannuaire-administration/exports/csv"
)
# Catégorie DILA correspondant aux services de l'État (versant FPE).
CATEGORIE_FPE = "SI"


class DilaOrganismeGateway(IOrganismeGateway):
    def __init__(self, timeout: int = 120):
        self.timeout = timeout

    def find_resource(self) -> OrganismeImportResource:
        return OrganismeImportResource(url=DILA_EXPORT_URL, millesime=date.today())

    def stream_organismes(
        self, resource: OrganismeImportResource
    ) -> Iterator[OrganismeData]:
        rows = self._fetch_rows(resource.url)
        parent_of = self._build_parent_of(rows)

        for row in rows:
            if row.get("categorie") != CATEGORIE_FPE:
                continue
            external_id = row.get("id")
            if not external_id:
                continue
            data = dict(row)
            data["parent_id"] = parent_of.get(external_id, "")
            yield OrganismeData(
                referentiel=OrganismeReferentiel.DILA,
                external_id=external_id,
                data=data,
            )

    @staticmethod
    def _build_parent_of(rows: list[dict]) -> dict[str, str]:
        # Le champ "hierarchie" d'un service liste ses propres enfants
        # ("Service Fils") : on reconstruit donc la relation inverse
        # enfant -> parent.
        parent_of: dict[str, str] = {}
        for row in rows:
            row_id = row.get("id")
            hierarchie = row.get("hierarchie")
            if not row_id or not hierarchie:
                continue
            try:
                items = json.loads(hierarchie)
            except (TypeError, ValueError):
                continue
            for item in items:
                service = item.get("service")
                if service:
                    parent_of[service] = row_id
        return parent_of

    def _fetch_rows(self, url: str) -> list[dict]:
        try:
            response = httpx.get(
                url,
                params={"lang": "fr", "timezone": "Europe/Paris", "delimiter": ";"},
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as err:
            raise ExternalApiError(
                "Erreur lors du téléchargement de l'annuaire DILA",
                details={"url": url, "error": str(err)},
            ) from err

        reader = csv.DictReader(io.StringIO(response.text), delimiter=";")
        return list(reader)
