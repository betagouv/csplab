import csv
import io
import json
from collections import Counter
from datetime import date
from typing import Iterator

import httpx

from domain.gateways.organisme_gateway import IOrganismeGateway
from domain.value_objects.organisme import OrganismeData, OrganismeImportResource
from domain.value_objects.organisme_referentiel import OrganismeReferentiel
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.gateways.siret_matching import normalize_name

# Catégorie DILA correspondant aux services de l'État (versant FPE).
CATEGORIE_FPE = "SI"
# Other link types ("Autre hiérarchie") are not parent-child links.
CHILD_HIERARCHY_TYPE = "Service Fils"


class DilaOrganismeGateway(IOrganismeGateway):
    def __init__(self, export_url: str, timeout: int = 120):
        self.export_url = export_url
        self.timeout = timeout

    def find_resource(self) -> OrganismeImportResource:
        return OrganismeImportResource(url=self.export_url, millesime=date.today())

    def stream_organismes(
        self, resource: OrganismeImportResource
    ) -> Iterator[OrganismeData]:
        rows = self._fetch_rows(resource.url)
        parent_of = self._build_parent_of(rows)
        fpe_rows = [row for row in rows if row.get("categorie") == CATEGORIE_FPE]
        # Cleaning works in batches: only the gateway sees the whole export and
        # can count the services sharing the same name.
        homonyms = Counter(normalize_name(row.get("nom") or "") for row in fpe_rows)

        for row in fpe_rows:
            external_id = row.get("id")
            if not external_id:
                continue
            data = dict(row)
            data["ancestors"] = self._ancestors(external_id, parent_of)
            data["homonyms"] = homonyms[normalize_name(row.get("nom") or "")]
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
                if service and item.get("type_hierarchie") == CHILD_HIERARCHY_TYPE:
                    parent_of[service] = row_id
        return parent_of

    @staticmethod
    def _ancestors(external_id: str, parent_of: dict[str, str]) -> list[str]:
        """External ids of the ancestors, from the closest to the furthest."""
        ancestors: list[str] = []
        seen = {external_id}
        parent = parent_of.get(external_id)
        while parent and parent not in seen:
            ancestors.append(parent)
            seen.add(parent)
            parent = parent_of.get(parent)
        return ancestors

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
