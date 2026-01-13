#To test : 
#           export TALENTSOFT_BASE_URL="https://place-ep-recrute.talent-soft.com"
#           export TALENTSOFT_API_KEY="grant_type=client_credentials&client_id=XXX&client_secret=YYYYY"
import os
import requests

from apps.ingestion.config import TalentSoftConfig
from apps.ingestion.infrastructure.adapters.external.talentsoft.token_service import TalentSoftTokenService

# logger minimal: adapte selon ton projet si tu as déjà un logger service réel
from core.services.logger_interface import ILogger

class DummyLoggerService(ILogger):
    def get_logger(self, name: str):
        import logging
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(name)

def main() -> None:
    base_url = os.environ["TALENTSOFT_BASE_URL"]
    # on ne met pas de secret en dur dans un script
    api_key = os.getenv("TALENTSOFT_API_KEY", "")

    config = TalentSoftConfig(base_url=base_url, api_key=api_key)
    session = requests.Session()
    token_service = TalentSoftTokenService(config, DummyLoggerService(), session, timeout=30)

    token = token_service.get_access_token()
    print("OK token:")
    print("  token_type:", token.token_type)
    print("  access_token prefix:", token.access_token[:20], "...")
    print("  expires_at_epoch:", token.expires_at_epoch)

if __name__ == "__main__":
    main()
