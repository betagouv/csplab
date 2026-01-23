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

                    current_start += 1

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

## Save offers as JSON

```python
import json
from pathlib import Path

# Vérifications avant export
print(f"📊 About to export {len(sample_offers)} offers")
print(f"📋 Type of sample_offers: {type(sample_offers)}")

if sample_offers:
    print(f"✅ Sample offers is not empty")
    print(f"🔍 First offer keys: {list(sample_offers[0].keys()) if sample_offers else 'No offers'}")

    # Créer le dossier data s'il n'existe pas
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)

    # Export avec gestion d'erreurs
    try:
        with open('data/fixtures_talentsoft.json', 'w', encoding='utf-8') as file:
            json.dump(sample_offers, file, indent=4, ensure_ascii=False)

        print(f"✅ Successfully exported to fixtures_talentsoft.json")

        # Vérifier que le fichier a été créé
        json_file = Path('data/fixtures_talentsoft.json')
        if json_file.exists():
            file_size = json_file.stat().st_size
            print(f"📁 File created: {file_size / (1024*1024):.1f} MB")
        else:
            print("❌ File was not created!")

    except Exception as e:
        print(f"❌ Export failed: {e}")

else:
    print("❌ sample_offers is empty! Check the API extraction.")
```

## Load Data from Saved JSON File

```python
# Load data directly from saved JSON file
import json
import pandas as pd

# Load the saved offers
with open('data/fixtures_talentsoft.json', 'r') as file:
    loaded_offers = json.load(file)

print(f"Loaded {len(loaded_offers)} offers from JSON file")

# Parse the loaded offers
df_loaded = pd.DataFrame(loaded_offers)

print(f"Created DataFrame with {len(df_loaded)} rows and {len(df_loaded.columns)} columns")
print(f"Columns: {list(df_loaded.columns)}")

# Display first few rows
df_loaded.head()
```

## Explore for clean up and mapping to Offer Entity

```python
def offer_parser(item):
    external_id = item['reference']

    # Handle optional salaryRange field
    verse = None
    salary_range = item.get('salaryRange')
    if salary_range and salary_range.get('clientCode'):
        verse = salary_range['clientCode']

    # Handle optional country field
    countries = None
    if item.get('country'):
        countries = [country['label'] for country in item['country']]

    # Handle optional region field
    regions = None
    if item.get('region'):
        regions = [region['label'] for region in item['region']]

    # Handle optional department field
    departments = None
    if item.get('department'):
        departments = [dept.get('clientCode') for dept in item['department']]

    return {
        'external_id': item['reference'],
        'verse': verse,
        'title': item.get('title'),
        'role': item.get('description1'),
        'profile': item.get('description2'),
        'organisation': item.get('organisationName'),
        'country': countries,
        'region': regions,
        'department': departments,
        'offer_url': item.get('offerUrl'),
        'publication_date': item.get('startPublicationDate'),
    }
```

```python
offers = [offer_parser(item) for item in sample_offers]
df = pd.DataFrame(offers)
```
