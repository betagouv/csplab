import httpx

from domain.gateways.siret_lookup_gateway import ISiretLookupGateway
from domain.value_objects.siret_candidate import SiretCandidate
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.gateways.rate_limiter import RateLimiter

_CANDIDATES_PER_SEARCH = 5


class RechercheEntreprisesGateway(ISiretLookupGateway):
    """Searches active legal units by name or SIRET via the Recherche
    Entreprises API.

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

    def search(self, query: str) -> list[SiretCandidate]:
        self._rate_limiter.wait()
        try:
            response = httpx.get(
                self._search_url,
                params={
                    "q": query,
                    "per_page": _CANDIDATES_PER_SEARCH,
                    "etat_administratif": "A",
                    "minimal": "true",
                    "include": "siege",
                },
                timeout=self._timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as err:
            raise ExternalApiError(
                "Recherche Entreprises API lookup failed",
                api_name="recherche_entreprises",
                details={"query": query, "error": str(err)},
            ) from err

        return [
            SiretCandidate(
                siret=(result.get("siege") or {}).get("siret") or None,
                siren=result.get("siren") or "",
                denomination=result.get("nom_complet") or "",
                nature_juridique=result.get("nature_juridique") or None,
            )
            for result in response.json().get("results") or []
        ]
