from collections import defaultdict

from domain.gateways.metiers_gateway import IMetiersGateway
from infrastructure.external_gateways.base_web_gateway import BaseWebGateway

# MAX_PAGE_SIZE of the web API: the whole referentiel fits in two pages.
_PAGE_SIZE = 1_000


class WebMetiersGateway(BaseWebGateway, IMetiersGateway):
    async def fetch_metiers_multi_domaines(self) -> set[str]:
        domains_by_code: defaultdict[str, set[str]] = defaultdict(set)
        page = 1
        while True:
            response = await self._get(f"/metiers?taille={_PAGE_SIZE}&page={page}")
            body = response.json()
            for metier in body["results"]:
                domains_by_code[metier["code_emploi_csp"]].add(
                    metier["domaine_fonctionnel_code"]
                )
            if not body.get("next"):
                break
            page += 1
        return {code for code, domains in domains_by_code.items() if len(domains) > 1}
