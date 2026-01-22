# TalentSoft DTO explorer

Ce notebook permet d'étudier les DTOs des données réelles de l'API TalentSoft afin d'affiner le service clean offers.

## Setup

```python
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from IPython.display import JSON
import pandas as pd

# Add tycho to path for imports
sys.path.append(str(Path.cwd().parent / "tycho"))

from infrastructure.external_gateways.talentsoft_client import TalentsoftFrontClient
from infrastructure.gateways.shared.logger import LoggerService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TALENTSOFT_BASE_URL = os.getenv("TALENTSOFT_BASE_URL")
TALENTSOFT_CLIENT_ID = os.getenv("TALENTSOFT_CLIENT_ID")
TALENTSOFT_CLIENT_SECRET = os.getenv("TALENTSOFT_CLIENT_SECRET")

print(f"Base URL: {TALENTSOFT_BASE_URL}")
print(f"Client ID: {TALENTSOFT_CLIENT_ID[:10]}..." if TALENTSOFT_CLIENT_ID else "No Client ID")
```

## Local Corrected DTO

```python
# Only the corrected DTO - we'll use TalentsoftFrontClient as-is
from pydantic import BaseModel, Field
from domain.types import JsonDataType

class LocalTalentsoftOffersResponse(BaseModel):
    """Corrected offers response with proper pagination field alias."""
    data: JsonDataType
    pagination: JsonDataType = Field(alias="_pagination")

# Corrected endpoints (without leading slash)
TOKEN_ENDPOINT = "api/token"
OFFERS_ENDPOINT = "api/v2/offersummaries"

print("✅ Local corrected DTO and endpoints loaded")
```

## Fetch Sample Offers with TalentsoftFrontClient

```python
from pydantic import HttpUrl

async def fetch_sample_offers(limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch sample offers from TalentSoft API using corrected implementation."""

    # Initialize logger
    logger_service = LoggerService()

    # Validate and convert base_url to HttpUrl
    if not TALENTSOFT_BASE_URL:
        raise ValueError("TALENTSOFT_BASE_URL is required")

    base_url = HttpUrl(TALENTSOFT_BASE_URL)

    try:
        # Use TalentsoftFrontClient with async context manager
        async with TalentsoftFrontClient(
            base_url=base_url,
            client_id=TALENTSOFT_CLIENT_ID,
            client_secret=TALENTSOFT_CLIENT_SECRET,
            logger_service=logger_service,
            timeout=30
        ) as client:
            print("TalentSoft client initialized")

            # Use corrected approach with pagination to get more offers
            all_offers = []
            current_start = 1
            batch_size = 2500

            while len(all_offers) < limit:
                try:
                    # Make direct HTTP request using corrected endpoints
                    url = f"{client.base_url}{OFFERS_ENDPOINT}"
                    params = {"count": min(batch_size, limit - len(all_offers)), "start": current_start}

                    token = await client.get_access_token()
                    headers = client._build_auth_headers(token)

                    response = await client.get(url, headers=headers, params=params)
                    response.raise_for_status()

                    # Use corrected DTO
                    typed_response = LocalTalentsoftOffersResponse.model_validate(response.json())
                    offers = typed_response.data
                    pagination = typed_response.pagination

                    if not offers:
                        print("No more offers available")
                        break

                    all_offers.extend(offers)
                    print(f"Fetched batch: {len(offers)} offers (Total: {len(all_offers)})")

                    # Check if we have more data
                    has_more = bool(pagination.get("hasMore", False))
                    if not has_more:
                        print("API indicates no more pages available")
                        break

                    current_start += batch_size

                except Exception as batch_error:
                    print(f"Error in batch starting at {current_start}: {batch_error}")
                    break

            # Limit to requested number
            sample_offers = all_offers[:limit] if all_offers else []

            print(f"Final result: {len(sample_offers)} offers")

            # Display structure of first offer
            if sample_offers:
                first_offer = sample_offers[0]
                print(f"\nFirst offer structure:")
                print(f"Keys: {list(first_offer.keys())}")

                # Show sample values (anonymized)
                for key, value in first_offer.items():
                    if isinstance(value, str) and len(value) > 50:
                        print(f"  {key}: {value[:50]}...")
                    else:
                        print(f"  {key}: {value}")

            return sample_offers

    except Exception as e:
        print(f"Error fetching offers: {e}")
        return []

# Fetch sample data
sample_offers = await fetch_sample_offers(limit=60000)
```

```python
with open('data/fixtures_talentsoft.json', 'w') as file:
    json.dump(sample_offers, file, indent=4)
JSON(sample_offers)
```

```python
def offer_parser(item):
    external_id = item['reference']
    verse = None
    if item['salaryRange'] and item['salaryRange']['clientCode']:
        verse = item['salaryRange']['clientCode']

    countries = None
    if item['country']:
        countries = [country['label'] for country in item['country']]

    regions = None
    if item['region']:
        regions = [region['label'] for region in item['region']]

    departments = None
    if item['department']:
        departments = [region['clientCode'] for region in item['department']]

    return {
        'external_id': item['reference'],
        'verse': verse,
        'title': item['title'],
        'role': item['description1'],
        'profile': item['description2'],
        'organisation': item['organisationName'],
        'country': countries,
        'region': regions,
        'department': departments,
        'offer_url': item['offerUrl'],
        'publication_date': item['startPublicationDate'],
    }
```

```python
offers = [offer_parser(item) for item in sample_offers]
df = pd.DataFrame(offers)
```

```python
df.head()
```
