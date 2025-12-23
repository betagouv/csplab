import os

from apps.ingestion.config import TalentSoftConfig
from apps.ingestion.infrastructure.adapters.external.talentsoft.client import TalentSoftHttpClient
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
    client = TalentSoftHttpClient(config=config, logger_service=DummyLoggerService(), timeout=30)

    resp = client.request("GET", "/api/v2/offersummaries")
    print("Status:", resp.status_code)
    resp.raise_for_status()
    payload = resp.json()

    print("Normalized keys:", list(payload.keys()))
    offers = payload.get("offers") or []
    print("Normalized offers count:", len(offers))
    if offers:
        first = offers[0]
        print("First normalized offer:")
        for k, v in first.items():
            print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
