from collections import defaultdict

from infrastructure.external_gateways.base_web_gateway import BaseWebGateway


class WebMetiersGateway(BaseWebGateway):
    async def fetch_metiers_multi_domaines(self) -> set[str]:
        domains_by_code: defaultdict[str, set[str]] = defaultdict(set)
        page = 1
        while True:
            body = (await self._get(f"/metiers?taille=1000&page={page}")).json()
            for metier in body["results"]:
                domains_by_code[metier["code_emploi_csp"]].add(
                    metier["domaine_fonctionnel_code"]
                )
            if not body["next"]:
                return {code for code, d in domains_by_code.items() if len(d) > 1}
            page += 1
