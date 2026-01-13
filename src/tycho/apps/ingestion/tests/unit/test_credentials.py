#To test : export TALENTSOFT_API_KEY="grant_type=client_credentials&client_id=XXX&client_secret=YYYYY"
import os
from apps.ingestion.infrastructure.adapters.external.talentsoft.credentials import parse_credentials

def main() -> None:
    api_key = os.getenv("TALENTSOFT_API_KEY", "")
    creds = parse_credentials(api_key)
    print("OK credentials:")
    print("  grant_type:", creds.grant_type)
    print("  client_id:", creds.client_id[:4] + "..." if creds.client_id else "")
    print("  client_secret:", "****" if creds.client_secret else "")

if __name__ == "__main__":
    main()