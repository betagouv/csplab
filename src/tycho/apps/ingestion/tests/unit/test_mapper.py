import json
from pathlib import Path

from apps.ingestion.infrastructure.adapters.external.talentsoft.offersummaries_mapper import (
    OfferSummariesMapper,
)


def main() -> None:
    # tu crées ce fichier en copiant une vraie réponse JSON de l'API
    raw = json.loads(
        Path("scripts/talentsoft/offersummaries_sample.json").read_text(
            encoding="utf-8"
        )
    )

    normalized = OfferSummariesMapper.map_payload(raw)

    offers = normalized.get("offers") or []
    print("Normalized offers:", len(offers))
    if offers:
        print("First normalized offer:", offers[0])


if __name__ == "__main__":
    main()
