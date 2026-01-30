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

## Analyse data


### Analyse localisation format

```python
import json
import pandas as pd
import numpy as np

# Charger les données
with open('data/fixtures_talentsoft.json', 'r') as file:
    loaded_offers = json.load(file)

print(f"📊 Analyzing {len(loaded_offers)} offers")

# Analyser les longueurs des tableaux
country_lengths = []
region_lengths = []
department_lengths = []

for offer in loaded_offers:
    # Country
    country = offer.get('country', [])
    country_lengths.append(len(country) if country else 0)

    # Region
    region = offer.get('region', [])
    region_lengths.append(len(region) if region else 0)

    # Department
    department = offer.get('department', [])
    department_lengths.append(len(department) if department else 0)

# Statistiques
print("\n🌍 COUNTRY lengths:")
print(f"  Min: {min(country_lengths)}, Max: {max(country_lengths)}")
print(f"  Mean: {np.mean(country_lengths):.2f}")
print(f"  Distribution: {pd.Series(country_lengths).value_counts().sort_index()}")

print("\n🏞️ REGION lengths:")
print(f"  Min: {min(region_lengths)}, Max: {max(region_lengths)}")
print(f"  Mean: {np.mean(region_lengths):.2f}")
print(f"  Distribution: {pd.Series(region_lengths).value_counts().sort_index()}")

print("\n🏛️ DEPARTMENT lengths:")
print(f"  Min: {min(department_lengths)}, Max: {max(department_lengths)}")
print(f"  Mean: {np.mean(department_lengths):.2f}")
print(f"  Distribution: {pd.Series(department_lengths).value_counts().sort_index()}")

# Exemples d'offers avec plusieurs valeurs
print("\n🔍 EXAMPLES with multiple values:")
for i, offer in enumerate(loaded_offers[:100]):  # Check first 100
    country = offer.get('country', [])
    region = offer.get('region', [])
    department = offer.get('department', [])

    if len(country) > 1 or len(region) > 1 or len(department) > 1:
        print(f"Offer {i}: country={len(country)}, region={len(region)}, dept={len(department)}")
        if len(country) > 1:
            print(f"  Countries: {[c.get('label') for c in country]}")
        if len(region) > 1:
            print(f"  Regions: {[r.get('label') for r in region]}")
        if len(department) > 1:
            print(f"  Departments: {[d.get('label') for d in department]}")
```

### Analyse contract type format

```python
import json
import pandas as pd
from collections import Counter

# Charger les données
with open('data/fixtures_talentsoft.json', 'r') as file:
    loaded_offers = json.load(file)

print(f"📊 Analyzing contractType on {len(loaded_offers)} offers")

# Extraire tous les contractType
contract_types = []
contract_type_details = []

for offer in loaded_offers:
    contract_type = offer.get('contractType')

    if contract_type:
        # Récupérer le label
        label = contract_type.get('label', 'No label')
        contract_types.append(label)

        # Récupérer tous les détails
        contract_type_details.append({
            'label': label,
            'clientCode': contract_type.get('clientCode'),
            'id': contract_type.get('id'),
            'full_object': contract_type
        })
    else:
        contract_types.append('NULL')
        contract_type_details.append({'label': 'NULL', 'clientCode': None, 'id': None})

# Statistiques des labels
print("\n📋 CONTRACT TYPE LABELS:")
label_counts = Counter(contract_types)
for label, count in label_counts.most_common():
    percentage = (count / len(loaded_offers)) * 100
    print(f"  '{label}': {count:,} offers ({percentage:.1f}%)")

# Analyser les clientCode
print("\n🔑 CLIENT CODES:")
client_codes = [detail['clientCode'] for detail in contract_type_details if detail['clientCode']]
if client_codes:
    code_counts = Counter(client_codes)
    for code, count in code_counts.most_common():
        percentage = (count / len(loaded_offers)) * 100
        print(f"  '{code}': {count:,} offers ({percentage:.1f}%)")
else:
    print("  No clientCode found")

# Exemples détaillés
print("\n🔍 DETAILED EXAMPLES:")
unique_contract_types = {}
for detail in contract_type_details:
    label = detail['label']
    if label not in unique_contract_types and label != 'NULL':
        unique_contract_types[label] = detail['full_object']

for label, full_obj in list(unique_contract_types.items())[:5]:
    print(f"  '{label}':")
    print(f"    Full object: {full_obj}")
```

### Analysis of professionalCategory field

```python
import json
import pandas as pd
from collections import Counter

# Charger les données
with open('data/fixtures_talentsoft.json', 'r') as file:
    loaded_offers = json.load(file)

print(f"📊 Analyzing professionalCategory on {len(loaded_offers)} offers")

# Extraire toutes les professionalCategory
categories = []
category_details = []

for offer in loaded_offers:
    professional_category = offer.get('professionalCategory')

    if professional_category:
        # Récupérer le clientCode
        client_code = professional_category.get('clientCode')
        label = professional_category.get('label', 'No label')

        categories.append(client_code)
        category_details.append({
            'clientCode': client_code,
            'label': label,
            'full_object': professional_category
        })
    else:
        categories.append(None)
        category_details.append({'clientCode': None, 'label': None})

# Statistiques des clientCode
print("\n📋 PROFESSIONAL CATEGORY CLIENT CODES:")
code_counts = Counter(categories)
for code, count in code_counts.most_common():
    percentage = (count / len(loaded_offers)) * 100
    print(f"  '{code}': {count:,} offers ({percentage:.1f}%)")

# Analyser les labels correspondants
print("\n🏷️ LABELS by CLIENT CODE:")
unique_categories = {}
for detail in category_details:
    client_code = detail['clientCode']
    if client_code and client_code not in unique_categories:
        unique_categories[client_code] = detail

for client_code, detail in unique_categories.items():
    print(f"  '{client_code}' → '{detail['label']}'")

# Exemples détaillés
print("\n🔍 DETAILED EXAMPLES:")
for client_code, detail in list(unique_categories.items())[:10]:
    print(f"  {client_code}:")
    print(f"    Label: {detail['label']}")
    print(f"    Full object: {detail['full_object']}")

# Croiser avec contractType
print("\n🔄 CROSS ANALYSIS: professionalCategory × contractType")
cross_data = []

for offer in loaded_offers:
    # ProfessionalCategory
    prof_cat = offer.get('professionalCategory')
    prof_cat_code = prof_cat.get('clientCode') if prof_cat else None

    # ContractType
    contract_type = offer.get('contractType')
    contract_type_code = contract_type.get('clientCode') if contract_type else None

    cross_data.append({
        'professionalCategory': prof_cat_code,
        'contractType': contract_type_code
    })

df_cross = pd.DataFrame(cross_data)
cross_table = pd.crosstab(
    df_cross['professionalCategory'],
    df_cross['contractType'],
    margins=True,
    dropna=False
)
print(cross_table)
```

### Analysis of all fields on real and deduction of DTOs

```python
import json
import pandas as pd
from collections import defaultdict, Counter
from typing import Any, Dict, List, Set, Union
from datetime import datetime

# Charger les données
with open('data/fixtures_talentsoft.json', 'r') as file:
    loaded_offers = json.load(file)

print(f"📊 Analyzing structure of {len(loaded_offers)} TalentSoft offers")

class FieldAnalyzer:
    def __init__(self):
        self.field_stats = defaultdict(lambda: {
            'count': 0,
            'null_count': 0,
            'types': Counter(),
            'sample_values': set(),
            'max_length': 0,
            'is_array': False,
            'array_lengths': Counter(),
            'nested_structure': None
        })

    def analyze_value(self, value: Any, field_path: str):
        """Analyse une valeur et met à jour les statistiques."""
        stats = self.field_stats[field_path]
        stats['count'] += 1

        if value is None:
            stats['null_count'] += 1
            stats['types']['NoneType'] += 1
            return

        # Type de base
        value_type = type(value).__name__
        stats['types'][value_type] += 1

        # Analyse selon le type
        if isinstance(value, str):
            stats['max_length'] = max(stats['max_length'], len(value))
            if len(stats['sample_values']) < 10:
                stats['sample_values'].add(value[:100])  # Limiter la longueur

        elif isinstance(value, (int, float)):
            if len(stats['sample_values']) < 10:
                stats['sample_values'].add(value)

        elif isinstance(value, bool):
            stats['sample_values'].add(value)

        elif isinstance(value, list):
            stats['is_array'] = True
            stats['array_lengths'][len(value)] += 1

            # Analyser les éléments du tableau
            for i, item in enumerate(value):
                if i < 3:  # Analyser seulement les 3 premiers éléments
                    self.analyze_value(item, f"{field_path}[{i}]")

        elif isinstance(value, dict):
            # Analyser les champs de l'objet imbriqué
            if stats['nested_structure'] is None:
                stats['nested_structure'] = set()

            for key, nested_value in value.items():
                stats['nested_structure'].add(key)
                self.analyze_value(nested_value, f"{field_path}.{key}")

    def analyze_offers(self, offers: List[Dict]):
        """Analyse toutes les offers."""
        for i, offer in enumerate(offers):
            if i % 5000 == 0:
                print(f"  Processing offer {i:,}/{len(offers):,}")

            self.analyze_object(offer, "")

    def analyze_object(self, obj: Dict, prefix: str):
        """Analyse récursivement un objet."""
        for key, value in obj.items():
            field_path = f"{prefix}.{key}" if prefix else key
            self.analyze_value(value, field_path)

    def get_python_type(self, field_path: str) -> str:
        """Déduit le type Python approprié."""
        stats = self.field_stats[field_path]

        if stats['null_count'] > 0:
            is_optional = True
        else:
            is_optional = False

        # Type le plus fréquent
        most_common_type = stats['types'].most_common(1)[0][0] if stats['types'] else 'str'

        # Conversion vers types Python/Pydantic
        type_mapping = {
            'str': 'str',
            'int': 'int',
            'float': 'float',
            'bool': 'bool',
            'list': 'List[Any]',  # À affiner selon le contenu
            'dict': 'Dict[str, Any]',  # À affiner selon la structure
            'NoneType': 'Optional[str]'
        }

        python_type = type_mapping.get(most_common_type, 'Any')

        # Gestion des tableaux
        if stats['is_array']:
            if stats['array_lengths']:
                max_length = max(stats['array_lengths'].keys())
                if max_length <= 1:
                    python_type = f"Optional[List[Dict[str, Any]]]"
                else:
                    python_type = f"List[Dict[str, Any]]"

        # Optionalité
        if is_optional and not python_type.startswith('Optional'):
            python_type = f"Optional[{python_type}]"

        return python_type

    def generate_report(self):
        """Génère un rapport complet."""
        print("\n" + "="*80)
        print("📋 TALENTSOFT STRUCTURE ANALYSIS REPORT")
        print("="*80)

        # Trier les champs par fréquence
        sorted_fields = sorted(
            self.field_stats.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )

        for field_path, stats in sorted_fields:
            if '.' not in field_path and '[' not in field_path:  # Champs de premier niveau seulement
                self.print_field_analysis(field_path, stats)

        print("\n" + "="*80)
        print("🏗️ NESTED OBJECTS ANALYSIS")
        print("="*80)

        # Analyser les objets imbriqués
        nested_objects = {}
        for field_path, stats in sorted_fields:
            if stats['nested_structure']:
                nested_objects[field_path] = stats

        for field_path, stats in nested_objects.items():
            print(f"\n📦 {field_path}:")
            print(f"  Nested fields: {sorted(stats['nested_structure'])}")

            # Analyser les champs imbriqués
            for nested_field in sorted(stats['nested_structure']):
                nested_path = f"{field_path}.{nested_field}"
                if nested_path in self.field_stats:
                    nested_stats = self.field_stats[nested_path]
                    python_type = self.get_python_type(nested_path)
                    presence = (nested_stats['count'] / stats['count']) * 100
                    print(f"    {nested_field}: {python_type} ({presence:.1f}% present)")

    def print_field_analysis(self, field_path: str, stats: Dict):
        """Affiche l'analyse d'un champ."""
        total_offers = len(loaded_offers)
        presence_pct = (stats['count'] / total_offers) * 100
        null_pct = (stats['null_count'] / stats['count']) * 100 if stats['count'] > 0 else 0

        python_type = self.get_python_type(field_path)

        print(f"\n🔍 {field_path}:")
        print(f"  Type: {python_type}")
        print(f"  Presence: {stats['count']:,}/{total_offers:,} ({presence_pct:.1f}%)")
        print(f"  Null values: {stats['null_count']:,} ({null_pct:.1f}%)")
        print(f"  Types found: {dict(stats['types'])}")

        if stats['sample_values']:
            sample_values = list(stats['sample_values'])[:5]
            print(f"  Sample values: {sample_values}")

        if stats['is_array']:
            print(f"  Array lengths: {dict(stats['array_lengths'])}")

        if isinstance(stats['max_length'], int) and stats['max_length'] > 0:
            print(f"  Max string length: {stats['max_length']}")

# Lancer l'analyse
analyzer = FieldAnalyzer()
analyzer.analyze_offers(loaded_offers)
analyzer.generate_report()

print(f"\n✅ Analysis complete! Ready to generate Pydantic DTOs.")
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

    #contrat_type
    contract_type = None
    contract_type_object = item.get('contractType')
    if contract_type_object and contract_type_object.get('clientCode'):
        contract_type = contract_type_object['clientCode']

    #category
    category = None

    # Handle optional country field
    country = None
    if item.get('country') and len(item['country']) == 1:
        country = item['country'][0]['clientCode']

    # Handle optional region field
    region = None
    if item.get('region') and len(item['region']) == 1:
        regions = item['region'][0]['clientCode']

    # Handle optional department field
    department = None
    if item.get('department') and len(item['department']) == 1:
        department = item['department'][0]['clientCode']

    return {
        'external_id': item['reference'],
        'verse': verse,
        'category': category,
        'contract_type': contract_type,
        'title': item.get('title'),
        'mission': item.get('description1'),
        'profile': item.get('description2'),
        'organisation': item.get('organisationName'),
        'country': country,
        'region': region,
        'department': department,
        'offer_url': item.get('offerUrl'),
        'publication_date': item.get('startPublicationDate'),
        'beginning_date': item.get('beginningDate'),
    }
```

```python
offers = [offer_parser(item) for item in loaded_offers]
df = pd.DataFrame(offers)
df.head()
```

```python
from pydantic import BaseModel, Field
from typing import Optional, List
import json

# =============================================================================
# TALENTSOFT DTOs - Corrected version
# =============================================================================

class TalentsoftCodedObject(BaseModel):
    """Base class for all TalentSoft coded objects."""
    code: int
    clientCode: str
    label: str
    active: bool
    parentCode: Optional[int] = None
    type: str
    parentType: str = ""
    hasChildren: bool = False

class TalentsoftLink(BaseModel):
    """TalentSoft _links object."""
    href: str
    rel: str

class TalentsoftOffer(BaseModel):
    """Complete TalentSoft offer DTO."""

    # Mandatory fields
    reference: str
    isTopOffer: bool
    title: str
    organisationName: str
    organisationDescription: str
    organisationLogoUrl: str
    modificationDate: str
    startPublicationDate: str
    offerUrl: str

    # Mandatory coded objects
    offerFamilyCategory: TalentsoftCodedObject
    contractTypeCountry: TalentsoftCodedObject

    # Mandatory arrays (can be empty)
    geographicalLocation: List[TalentsoftCodedObject] = []
    country: List[TalentsoftCodedObject] = []
    region: List[TalentsoftCodedObject] = []
    department: List[TalentsoftCodedObject] = []
    _links: List[TalentsoftLink] = []

    # Optional text fields
    location: Optional[str] = None
    description1: Optional[str] = None
    description2: Optional[str] = None
    description1Formatted: Optional[str] = None
    description2Formatted: Optional[str] = None
    beginningDate: Optional[str] = None
    contractDuration: Optional[str] = None

    # Optional coded objects
    contractType: Optional[TalentsoftCodedObject] = None
    salaryRange: Optional[TalentsoftCodedObject] = None
    professionalCategory: Optional[TalentsoftCodedObject] = None

    # Optional coordinates
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # Optional redirect URLs
    urlRedirectionEmployee: Optional[str] = None
    urlRedirectionApplicant: Optional[str] = None

class TalentsoftOffersResponse(BaseModel):
    """TalentSoft offers API response."""
    data: List[TalentsoftOffer]
    pagination: dict = Field(alias="_pagination")

# =============================================================================
# TESTING
# =============================================================================

print("🧪 Testing TalentSoft DTOs...")

# Load and test
with open('data/fixtures_talentsoft.json', 'r') as file:
    sample_offers = json.load(file)

# Test first offer
if sample_offers:
    try:
        first_offer = TalentsoftOffer.model_validate(sample_offers[0])
        print(f"✅ Successfully validated offer: {first_offer.reference}")
        print(f"   Title: {first_offer.title}")
        print(f"   Organization: {first_offer.organisationName}")
    except Exception as e:
        print(f"❌ Validation failed: {e}")

print("🎉 DTOs ready!")
```

```python

```
