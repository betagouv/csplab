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
# Corrected endpoints (without leading slash)
TOKEN_ENDPOINT = "api/token"
OFFERS_ENDPOINT = "api/v2/offersummaries"

print("✅ Local corrected DTO and endpoints loaded")
```

## Fetch Sample Offers with TalentsoftFrontClient

```python
import httpx
import asyncio
from typing import List, Dict, Any
import json
from datetime import datetime

class SimpleTalentsoftClient:
    def __init__(self, base_url: str, client_id: str, client_secret: str):
        self.base_url = base_url.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expires_at = None

    async def get_token(self):
        if self.token and self.token_expires_at and datetime.now().timestamp() < self.token_expires_at:
            return self.token

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                }
            )
            response.raise_for_status()
            token_data = response.json()

            self.token = token_data["access_token"]
            self.token_expires_at = datetime.now().timestamp() + token_data["expires_in"] - 30

            return self.token

    async def get_offers_summaries(self, start: int = 1, count: int = 100):
        token = await self.get_token()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v2/offersummaries",
                headers={"Authorization": f"Bearer {token}"},
                params={"start": start, "count": count}
            )
            response.raise_for_status()
            return response.json()

    async def get_offer_detail(self, reference: str):
        token = await self.get_token()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v2/offers/getoffer",
                headers={"Authorization": f"Bearer {token}"},
                params={"reference": reference}
            )
            response.raise_for_status()
            return response.json()

    async def get_offers_details_batch(self, limit: int = 100):
        print(f"🔍 Récupération de {limit} offres détaillées...")

        summaries_response = await self.get_offers_summaries(count=limit)
        offers_summaries = summaries_response.get("data", [])

        # 2. Récupérer les détails pour chaque offre
        detailed_offers = []

        for i, summary in enumerate(offers_summaries):
            try:
                reference = summary.get("reference")
                if reference:
                    detail = await self.get_offer_detail(reference)
                    detailed_offers.append(detail)

                    # Pause pour éviter de surcharger l'API
                    if i % 10 == 0 and i > 0:
                        await asyncio.sleep(1)

            except Exception as e:
                print(f"  ❌ Erreur pour {reference}: {e}")
                continue

        print(f"✅ {len(detailed_offers)} offres détaillées récupérées")
        return detailed_offers
```

## Save offers as JSON

```python
# Utilisation du client simplifié
async def main():
    # Configuration depuis les variables d'environnement
    client = SimpleTalentsoftClient(
        base_url=TALENTSOFT_BASE_URL,
        client_id=TALENTSOFT_CLIENT_ID,
        client_secret=TALENTSOFT_CLIENT_SECRET
    )

    # Récupérer 100 offres détaillées
    detailed_offers = await client.get_offers_details_batch(limit=100)

    # Sauvegarder les résultats
    with open('data/detailed_offers_sample.json', 'w', encoding='utf-8') as f:
        json.dump(detailed_offers, f, indent=2, ensure_ascii=False)

    print(f"💾 Sauvegardé dans data/detailed_offers_sample.json")

    # Analyser les offerFamilyCategory
    analyze_family_categories(detailed_offers)

def analyze_family_categories(offers: List[Dict]):
    print("\n🔍 ANALYSE DES OFFER FAMILY CATEGORIES")
    print("="*50)

    categories_found = 0
    categories_empty = 0
    categories_null = 0

    for offer in offers:
        family_cat = offer.get('offerFamilyCategory')

        if family_cat is None:
            categories_null += 1
            print(f"❌ NULL: {offer.get('reference', 'NO_REF')}")
        elif family_cat.get('clientCode') == "":
            categories_empty += 1
            print(f"⚠️  EMPTY: {offer.get('reference', 'NO_REF')} - {family_cat}")
        else:
            categories_found += 1
            print(f"✅ FOUND: {offer.get('reference', 'NO_REF')} - {family_cat.get('clientCode')}")

    print(f"\n📊 RÉSULTATS:")
    print(f"  - Catégories trouvées: {categories_found}")
    print(f"  - Catégories vides: {categories_empty}")
    print(f"  - Catégories null: {categories_null}")
    print(f"  - Total: {len(offers)}")

# Exécuter
await main()
```

## Load Data from Saved JSON File

```python
# Load data directly from saved JSON file
import json
import pandas as pd

# Load the saved offers
with open('data/detailed_offers_sample.json', 'r') as file:
    loaded_offers = json.load(file)

print(f"Loaded {len(loaded_offers)} offers from JSON file")

# Parse the loaded offers
df_loaded = pd.DataFrame(loaded_offers)

print(f"Created DataFrame with {len(df_loaded)} rows and {len(df_loaded.columns)} columns")
print(f"Columns: {list(df_loaded.columns)}")

# Display first few rows
df_clean = df_loaded[["title", "offerFamilyCategory"]]
df_clean["clientCode"] = df_loaded["offerFamilyCategory"].apply(lambda detail: detail["clientCode"])
df_clean["label"] = df_loaded["offerFamilyCategory"].apply(lambda detail: detail["label"])
df_clean
```
