<!-- #region -->
## Connecting to the Scalingo production database

__Prerequisites:__

- Scalingo CLI installed (`brew install scalingo`)
- SSH key added to your Scalingo account (`scalingo keys-add my-key ~/.ssh/id_ed25519.pub`)
- `SCALINGO_POSTGRESQL_URL` set in your environment (`~/.zshrc`)

__Step 1 — Load the SSH key into the agent__ (once per session):
```bash
ssh-add ~/.ssh/id_ed25519
```

__Step 2 — Open the tunnel__ (keep this terminal open):

```bash
scalingo --app csplab-web --region osc-fr1 db-tunnel $SCALINGO_POSTGRESQL_URL
```

__Step 3 — Connect from the notebook:__

<!-- #endregion -->

```python
import re
from urllib.parse import urlparse
from sqlalchemy import create_engine
import os

raw_url = os.getenv("SCALINGO_POSTGRESQL_URL", "")
parsed = urlparse(re.sub(r'^postgres(ql)?://', 'postgresql+psycopg2://', raw_url))

engine = create_engine(
    f"postgresql+psycopg2://{parsed.username}:{parsed.password}@127.0.0.1:10000{parsed.path}"
)
```

## Organismes depuis la BDD

```python
import pandas as pd

df = pd.read_sql("""
    SELECT
        id,
        external_id,
        created_at,
        -- Champs organisation top-level (TalentsoftOffer)
        raw_data->>'reference'               AS reference,
        raw_data->>'organisationName'        AS organisation_name,
        raw_data->>'organisationDescription' AS organisation_description,
        raw_data->>'organisationLogoUrl'     AS organisation_logo_url,
        -- Champs organisation imbriqués (TalentsoftOrganisation)
        raw_data->'organisation'->>'entityCode'          AS entity_code,
        raw_data->'organisation'->>'name'                AS org_name,
        raw_data->'organisation'->>'description'         AS org_description,
        raw_data->'organisation'->>'url'                 AS org_url,
        raw_data->'organisation'->>'phoneNumber'         AS phone_number,
        raw_data->'organisation'->>'postCode'            AS post_code,
        raw_data->'organisation'->>'parentName'          AS parent_name,
        raw_data->'organisation'->>'logoUrl'             AS logo_url,
        raw_data->'organisation'->>'maxDelayForConsent'  AS max_delay_for_consent,
        raw_data->'organisation'->>'retentionPeriod'     AS retention_period,
        raw_data->'organisation'->'geolocation'->>'latitude'  AS geo_lat,
        raw_data->'organisation'->'geolocation'->>'longitude' AS geo_lon
    FROM ingestion_rawdocument
    WHERE document_type = 'OFFERS'
""", engine)

df.head()
```

## Référentiel organismes depuis l'API Talentsoft

```python

```

```python
import httpx

BASE_URL = os.getenv("TALENTSOFT_BASE_URL", "")
CLIENT_ID = os.getenv("TALENTSOFT_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("TALENTSOFT_CLIENT_SECRET", "")

async def get_token(client: httpx.AsyncClient) -> str:
    token_resp = await client.post(
        f"{BASE_URL}/api/token",
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )
    return token_resp.json()["access_token"]


async def fetch_all(endpoint: str, page_size: int = 100) -> list:
    all_items = []
    start = 1

    async with httpx.AsyncClient() as client:
        token = await get_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        while True:
            resp = await client.get(
                f"{BASE_URL}{endpoint}",
                headers=headers,
                params={"start": start, "count": page_size},
            )
            resp.raise_for_status()

            data = resp.json()
            items = data.get("data", data) if isinstance(data, dict) else data
            pagination = data.get("_pagination", {}) if isinstance(data, dict) else {}

            if not items:
                break

            all_items.extend(items)
            has_more = pagination.get("hasMore", len(items) == page_size)

            if not has_more:
                break
            start += 1

    return all_items


raw_orgs = await fetch_all("/api/v2/referential/organisation")

# Structure réelle : TalentsoftCodedObject
# { code, clientCode, label, active, parentCode, type, parentType, hasChildren, _links }
def flatten_org(org: dict) -> dict:
    links = {lnk["rel"]: lnk["href"] for lnk in org.get("_links", [])}
    return {
        "code": org.get("code"),
        "clientCode": org.get("clientCode"),
        "label": org.get("label"),
        "active": org.get("active"),
        "parentCode": org.get("parentCode"),
        "type": org.get("type"),
        "parentType": org.get("parentType"),
        "hasChildren": org.get("hasChildren"),
        "link_children": links.get("children"),
        "link_detail": links.get("detail"),
    }

df_orgs = pd.DataFrame([flatten_org(o) for o in raw_orgs])
df_orgs.head()
```

```python
len(df_orgs)
```

```python
df_orgs[df_orgs["label"]=="Communes"]
```

```python
import plotly.express as px

fig = px.treemap(df_orgs, ids="code", names="label", parents="parentCode")
fig.show(renderer="iframe")
```

```python
# 1. Compter les offres par organisme (BDD)
df_counts = pd.read_sql("""
    SELECT
        raw_data->'organisation'->>'entityCode' AS entity_code,
        COUNT(*) AS offer_count
    FROM ingestion_rawdocument
    WHERE document_type = 'OFFERS'
      AND raw_data->'organisation'->>'entityCode' IS NOT NULL
    GROUP BY entity_code
""", engine)

# 2. Merger dans df_orgs (entityCode = clientCode)
df_viz = df_orgs.merge(
    df_counts,
    left_on="clientCode",
    right_on="entity_code",
    how="left"
).fillna({"offer_count": 0})

# 3. Treemap pondéré
fig = px.treemap(
    df_viz,
    ids="code",
    names="label",
    parents="parentCode",
    values="offer_count",       # taille des tuiles
    hover_data=["clientCode"],
)
fig.show(renderer="iframe")

```

## Comparaison referential vs raw_documents

```python
# entityCode dans les raw_documents = clientCode dans le référentiel
df_bdd = pd.read_sql("""
    SELECT DISTINCT
        raw_data->'organisation'->>'entityCode' AS entity_code
    FROM ingestion_rawdocument
    WHERE document_type = 'OFFERS'
      AND raw_data->'organisation'->>'entityCode' IS NOT NULL
""", engine)

# Ensembles de clientCode
client_codes_ref = set(df_orgs["clientCode"].dropna())
entity_codes_bdd = set(df_bdd["entity_code"].dropna())

only_in_ref = client_codes_ref - entity_codes_bdd
only_in_bdd = entity_codes_bdd - client_codes_ref
in_both      = client_codes_ref & entity_codes_bdd

print(f"Référentiel Talentsoft  : {len(client_codes_ref)} clientCodes distincts")
print(f"BDD raw_documents       : {len(entity_codes_bdd)} entityCodes distincts")
print(f"En commun               : {len(in_both)}")
print(f"Seulement dans le réf.  : {len(only_in_ref)}")
print(f"Seulement dans la BDD   : {len(only_in_bdd)}")
```

```python
# Merge pour voir le label Talentsoft à côté des offres BDD
df_merged = (
    df_bdd
    .merge(
        df_orgs[["clientCode", "code", "label", "active", "parentCode"]],
        left_on="entity_code",
        right_on="clientCode",
        how="left",
    )
)
print(f"Taux de match : {df_merged['label'].notna().mean():.1%}")
df_merged.head(20)
```
