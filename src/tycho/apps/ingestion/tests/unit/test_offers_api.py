import os

import requests

from apps.ingestion.config import TalentSoftConfig
from apps.ingestion.infrastructure.adapters.external.talentsoft.offersummaries_api import (
    OfferSummariesApi,
)
from apps.ingestion.infrastructure.adapters.external.talentsoft.token_service import (
    TalentSoftTokenService,
)
from core.services.logger_interface import ILogger


class DummyLoggerService(ILogger):
    def get_logger(self, name: str):
        import logging

        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(name)


def main() -> None:
    base_url = os.environ["TALENTSOFT_BASE_URL"]
    api_key = os.getenv("TALENTSOFT_API_KEY", "")

    config = TalentSoftConfig(base_url=base_url, api_key=api_key)
    session = requests.Session()

    token_service = TalentSoftTokenService(
        config, DummyLoggerService(), session, timeout=30
    )
    token = token_service.get_access_token()

    api = OfferSummariesApi(config, DummyLoggerService(), session, timeout=30)
    resp = api.fetch(bearer_token=token.access_token)

    print("Status:", resp.status_code)
    resp.raise_for_status()
    payload = resp.json()

    print("Keys:", list(payload.keys()))
    data = payload.get("data") or []
    print("Offers count:", len(data))
    if data:
        first = data[0]
        print("First offer reference:", first.get("reference"))
        print("First offer title:", first.get("title"))


if __name__ == "__main__":
    main()
