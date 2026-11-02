#!/usr/bin/env python
"""Lists the DILA services missing from data/dila_sirets.csv, with their
Recherche Entreprises candidates, for a human review before adding them to
the mapping (source "revue_manuelle", or "exclusion" with an empty SIRET).

Associative and private candidates are listed too: the import never retains
them automatically, only the mapping can.
"""

import argparse
import csv
import logging
import re
import sys

from api.config import get_settings
from domain.value_objects.siret_candidate import SiretCandidate
from infrastructure.external_gateways.dila_organisme_gateway import (
    DilaOrganismeGateway,
)
from infrastructure.external_gateways.recherche_entreprises_gateway import (
    RechercheEntreprisesGateway,
)
from infrastructure.gateways.organismes_cleaner import (
    DILA_SIRETS_CSV,
    load_dila_sirets,
)
from infrastructure.gateways.siret_matching import is_potential_employer, name_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COLUMNS = [
    "dila_id",
    "dila_name",
    "type_organisme",
    "potential_employer",
    "directory_siret",
    "query",
    "candidate_siret",
    "candidate_denomination",
    "candidate_nature_juridique",
    "candidate_category",
    "score",
]


def _category(candidate: SiretCandidate) -> str:
    if candidate.is_public:
        return "public"
    if candidate.is_associative:
        return "associative"
    return "private"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="-",
        help="Output CSV file (default: standard output)",
    )
    parser.add_argument(
        "--potential-employers-only",
        action="store_true",
        help="Only list potential employers, the services that would raise "
        "DilaSiretNotFound (otherwise every service, which takes longer)",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    settings = get_settings()
    dila_gateway = DilaOrganismeGateway(export_url=str(settings.dila_export_url))
    lookup_gateway = RechercheEntreprisesGateway(
        search_url=str(settings.recherche_entreprises_api_url),
        max_calls_per_second=settings.recherche_entreprises_rate_limit_per_second,
    )
    mapping = load_dila_sirets(settings.dila_sirets_csv_path or DILA_SIRETS_CSV)

    output = sys.stdout if args.output == "-" else open(args.output, "w", newline="")
    # Columns missing from a row (no candidate) are written empty.
    writer = csv.DictWriter(output, fieldnames=COLUMNS, delimiter=";", restval="")
    writer.writeheader()

    total = 0
    for organisme in dila_gateway.stream_organismes(dila_gateway.find_resource()):
        data = organisme.data
        if organisme.external_id in mapping:
            continue
        name = (data.get("nom") or "").strip()
        type_organisme = (data.get("type_organisme") or "").strip()
        potential_employer = is_potential_employer(name, type_organisme)
        if args.potential_employers_only and not potential_employer:
            continue

        directory_siret = re.sub(r"\s", "", data.get("siret") or "")
        if not directory_siret and (data.get("homonyms") or 0) > 1:
            # Generic name ("Secrétariat général"): no lookup.
            continue
        query = directory_siret or name
        row = {
            "dila_id": organisme.external_id,
            "dila_name": name,
            "type_organisme": type_organisme,
            "potential_employer": "yes" if potential_employer else "no",
            "directory_siret": directory_siret,
            "query": query,
        }
        try:
            candidates = lookup_gateway.search(query)
        except Exception:
            logger.warning("Lookup failed for %s", query, exc_info=True)
            continue

        total += 1
        if not candidates:
            writer.writerow(row)
        for candidate in sorted(
            candidates,
            key=lambda c: name_score(name, c.denomination),
            reverse=True,
        ):
            writer.writerow(
                row
                | {
                    "candidate_siret": candidate.siret or "",
                    "candidate_denomination": candidate.denomination,
                    "candidate_nature_juridique": candidate.nature_juridique or "",
                    "candidate_category": _category(candidate),
                    "score": f"{name_score(name, candidate.denomination):.2f}",
                }
            )

    if output is not sys.stdout:
        output.close()
    logger.info("Listed %d DILA services missing from the mapping", total)


if __name__ == "__main__":
    main()
