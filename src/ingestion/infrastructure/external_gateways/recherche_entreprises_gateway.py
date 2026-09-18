import logging

import httpx

from domain.gateways.siret_lookup_gateway import ISiretLookupGateway
from infrastructure.gateways.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)


class RechercheEntreprisesGateway(ISiretLookupGateway):
    """Looks up a SIRET by name via the Recherche Entreprises API.

    https://recherche-entreprises.api.gouv.fr/search?q=NOM

    Calls are throttled to respect the API's rate limit. Caching a given
    lookup by external_id is the caller's responsibility.
    """

    def __init__(
        self,
        max_calls_per_second: float,
        search_url: str = "https://recherche-entreprises.api.gouv.fr/search",
        timeout: int = 10,
    ) -> None:
        self._search_url = search_url
        self._timeout = timeout
        self._rate_limiter = RateLimiter(max_calls_per_second)

    def find_siret(self, nom: str) -> str | None:
        return self._fetch_siret(nom)

    def _fetch_siret(self, nom: str) -> str | None:
        self._rate_limiter.wait()
        try:
            response = httpx.get(
                self._search_url, params={"q": nom}, timeout=self._timeout
            )
            response.raise_for_status()
        except httpx.HTTPError as err:
            logger.warning(
                "Erreur lors de la recherche du SIRET pour %r via l'API "
                "Recherche Entreprises: %s",
                nom,
                err,
            )
            return None

        results = response.json().get("results") or []
        if not results:
            return None

        siege = results[0].get("siege") or {}
        return siege.get("siret") or None
