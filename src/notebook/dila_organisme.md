## API DILA | Exploration et stratégie d'intégration



## 1. Données disponibles ?


Cette API donne accès à deux grands référentiels :

1. **L'annuaire complet** de ~94 000 services publics français (coordonnées, horaires, missions…)

2. **La compétence géographique** des services locaux, permettant de savoir quel service (CPAM, CAF, mairie…) est compétent pour chaque commune de France (5,8 millions de liaisons)

C'est une API publique, sans authentification, très utile pour géolocaliser ou référencer des organismes publics.


```python
import httpx
from IPython.display import Markdown, display

resp = httpx.get(
    "https://api-lannuaire.service-public.fr/api/explore/v2.1/catalog/datasets",
    params={
        "offset": 0,
        "timezone": "UTC",
        "include_links": "false",
        "include_app_metas": "false",
    },
    headers={"accept": "application/json; charset=utf-8"},
    timeout=30,
)
resp.raise_for_status()
data = resp.json()

lines = [
    f"**Total datasets : {data['total_count']}**\n",
    "| Dataset ID | Nb enregistrements | Schéma modifié | Données traitées le | Champs disponibles |",
    "|---|---:|---|---|---|",
]

for ds in data["results"]:
    metas = ds.get("metas", {}).get("default", {})
    champs = ", ".join(f"`{f['name']}`" for f in ds.get("fields", []))
    modified     = (metas.get("modified") or "")[:10] or "—"
    data_proc    = (metas.get("data_processed") or "")[:10] or "—"
    lines.append(
        f"| `{ds['dataset_id']}` "
        f"| {metas.get('records_count', '—'):,} "
        f"| {modified} "
        f"| {data_proc} "
        f"| {champs} |"
    )

display(Markdown("\n".join(lines)))

```

Pour `api-lannuaire-administration`, une observation correspond à une valeur possible du champ **url_service_public**

```python
import io, json
import httpx
import pandas as pd

resp = httpx.get(
    "https://api-lannuaire.service-public.fr/api/explore/v2.1/catalog/datasets/api-lannuaire-administration/exports/csv",
    params={"lang": "fr", "timezone": "Europe/Paris", "delimiter": ";"},
    timeout=120,
)
df_dila_full = pd.read_csv(io.StringIO(resp.text), sep=";")
df_dila_full.to_csv("data/dila_annuaire.csv", index=False)

print(f"Nombre de lignes          : {len(df_dila_full):,}")
print(f"URL non nulles            : {df_dila_full['url_service_public'].notna().sum():,}")
print(f"URL distinctes            : {df_dila_full['url_service_public'].nunique():,}")
```

Exemple : https://lannuaire.service-public.gouv.fr/institutions-juridictions/f6d38468-d59e-42c0-9d54-1f8e573c1250


#### Les champs disponibles et d'intérêt sont les suivants.

* **id** : un identifiant unique (format UUID)

* l'**url_service_public** : permet de distinguer la FPT

* **nom :&#x20;**&#x70;eut servir pour pour un matching sémantique

* **type_organisme**

* **siren** / **siret** (non pertinent pour les feuilles qui correspondent aux bureaux par exemple)

* **date de création**

* **date de modification**

* **localisation (long / lat)** : peut servir pour un matching

* notion de parent / enfant qui peut être reconstruite à partir du champ **hierarchie**


```python
df_dila_full["type_organisme"].value_counts()
```

## 2. La structure proposée converge-t-elle avec la structure des entités dans CSP ?


### 2.1 Analyse de la structure du référenciel Organisation de TS

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
df_orgs = df_orgs[df_orgs["active"]==True]
df_orgs.columns
```

```python
len(df_orgs)
```

```python
async def fetch_detail(client: httpx.AsyncClient, headers: dict, url: str) -> dict:
    resp = await client.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

async def enrich_with_details(df: pd.DataFrame) -> pd.DataFrame:
    details = []
    async with httpx.AsyncClient() as client:
        token = await get_token(client)
        headers = {"Authorization": f"Bearer {token}"}
        for url in df["link_detail"].dropna():
            detail = await fetch_detail(client, headers, url)
            details.append(detail)
    return pd.DataFrame(details)

df_details = await enrich_with_details(df_orgs)
print(df_details.columns.tolist())

```

```python
import plotly.express as px

fig = px.treemap(df_orgs[df_orgs["active"]==True], ids="code", names="label", parents="parentCode")
fig.show(renderer="iframe")
```

```python

```

> ### Conclusion : dans le référenciel des organismes de TS, la notion parent / enfant (hierarchique) est centrale pour la FPE.


### 2.2 Analyse de la structure du référenciel Organisation de TS utilisée en pratique

<!-- #region -->
Connecting to the Scalingo production database

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

#### Organismes depuis la BDD

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
```

```python
df_counts = pd.read_sql("""
    SELECT
        raw_data->'organisation'->>'entityCode' AS entity_code,
        COUNT(*) AS offer_count
    FROM ingestion_rawdocument
    WHERE document_type = 'OFFERS'
      AND raw_data->'organisation'->>'entityCode' IS NOT NULL
    GROUP BY entity_code
""", engine)

df_viz = df_orgs.merge(
    df_counts,
    left_on="clientCode",
    right_on="entity_code",
    how="left"
).fillna({"offer_count": 0})

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

#### Filtre sur les noeuds / feuilles qui sont rattachés directement à au moins une offre

```python
df_avec_offres = df_orgs.merge(
    df_counts,
    left_on="clientCode",
    right_on="entity_code",
    how="inner"
).copy()

codes_avec_offres = set(df_avec_offres["code"])
df_avec_offres["parentCode"] = df_avec_offres["parentCode"].where(
    df_avec_offres["parentCode"].isin(codes_avec_offres), other=""
)

fig = px.treemap(
    df_avec_offres,
    ids="code",
    names="label",
    parents="parentCode",
    values="offer_count",
    hover_data=["clientCode"],
    title=f"Organismes avec au moins 1 offre ({len(df_avec_offres)} organismes)",
)
fig.show(renderer="iframe")
```

### 2.3 Analyse de la structure des données proposées par la DILA

```python
## Reconstitution parent/enfant (clé "service" dans hierarchie)
parent_of: dict[str, str] = {}
for _, row in df_dila_full[df_dila_full["hierarchie"].notna()].iterrows():
    try:
        for item in json.loads(row["hierarchie"]):
            if "service" in item:
                parent_of[item["service"]] = row["id"]
    except Exception:
        pass

df_dila_full["parent_id"] = df_dila_full["id"].map(parent_of).fillna("")
n = len(df_dila_full)
n_p = (df_dila_full["parent_id"] != "").sum()
print(f"Total : {n:,} | Avec parent : {n_p:,} ({n_p/n:.1%}) | Racines : {n - n_p:,}")

```

```python
import re

BASE = "https://lannuaire.service-public.gouv.fr/"
UUID_PATTERN = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'

def parse_url_path(url) -> dict:
    if not isinstance(url, str):
        return {"slug_1": None, "slug_2": None, "n_slugs": 0}
    # Enlever le préfixe et l'UUID final
    path = url.replace(BASE, "")
    path = re.sub(UUID_PATTERN, "", path).strip("/")
    slugs = [s for s in path.split("/") if s]
    return {
        "slug_1": slugs[0] if len(slugs) > 0 else None,
        "slug_2": slugs[1] if len(slugs) > 1 else None,
        "n_slugs": len(slugs),
    }

parsed_urls = df_dila_full["url_service_public"].apply(parse_url_path)
df_dila_full[["slug_1", "slug_2", "n_slugs"]] = pd.DataFrame(parsed_urls.tolist(), index=df_dila_full.index)

# Distribution de la structure
print("=== Nombre de slugs ===")
print(df_dila_full["n_slugs"].value_counts())

print("\n=== Top slug_1 (1er niveau) ===")
print(df_dila_full["slug_1"].value_counts().head(20))

print("\n=== Cas à 2 slugs : slug_1 + slug_2 ===")
print(df_dila_full[df_dila_full["n_slugs"] == 2][["slug_1", "slug_2"]].value_counts().head(20))

```

```python
REGIONS = {
    "auvergne-rhone-alpes", "occitanie", "nouvelle-aquitaine", "grand-est",
    "hauts-de-france", "bourgogne-franche-comte", "normandie", "ile-de-france",
    "centre-val-de-loire", "provence-alpes-cote-d-azur", "pays-de-la-loire",
    "bretagne", "corse"
}
DOM_TOM = {"la-reunion", "martinique", "guadeloupe", "guyane", "mayotte",
           "collectivites-d-outre-mer"}

def classify(row) -> str:
    if row["n_slugs"] == 2:
        return "Territorial (région/dép.)"
    elif row["slug_1"] == "gouvernement":
        return "FPE central"
    elif row["slug_1"] == "ambassades":
        return "FPE international"
    elif row["slug_1"] in DOM_TOM:
        return "Territorial (DOM-TOM)"
    elif row["n_slugs"] == 1 and row["slug_1"]:
        return f"Autre ({row['slug_1']})"
    return "Inconnu"

df_dila_full["nature"] = df_dila_full.apply(classify, axis=1)

# Croiser avec a_un_parent
summary = (
    df_dila_full
    .assign(a_un_parent=df_dila_full["parent_id"] != "")
    .groupby(["nature", "a_un_parent"])
    .size()
    .unstack(fill_value=0)
    .rename(columns={False: "orphelin", True: "avec_parent"})
    .assign(total=lambda d: d.sum(axis=1))
    .assign(pct_orphelin=lambda d: (d["orphelin"] / d["total"]).map("{:.1%}".format))
)
summary.sort_values("total", ascending=False)
```

```python
# Les 7 nœuds "Inconnu" sans parent
vrais_inconnus = df_dila_full[
    (df_dila_full["nature"] == "Inconnu") & (df_dila_full["parent_id"] == "")
]
vrais_inconnus.to_csv("data/dila_inconnus_orphelins.csv", index=False)
print(f"{len(vrais_inconnus)} lignes exportées")
display(vrais_inconnus[["id", "nom", "url_service_public", "siren", "parent_id"]])
```

> ### Toutes les administrations hors territorial ont un parent.

```python
# df_tree hors territorial (FPE + institutions + ambassades)
df_hors_terr = df_dila_full[
    (df_dila_full["nature"] != "Territorial (région/dép.)") &
    (df_dila_full["parent_id"] != "")
].copy()

# Ajouter les racines manquantes pour le treemap
parent_ids_manquants = set(df_hors_terr["parent_id"]) - set(df_hors_terr["id"])
df_parents_fpe = df_dila_full[df_dila_full["id"].isin(parent_ids_manquants)]
df_tree_fpe = pd.concat([df_hors_terr, df_parents_fpe]).drop_duplicates("id")

print(f"Nœuds hors territorial : {len(df_tree_fpe):,}")
print(df_tree_fpe["nature"].value_counts())

# Treemap
fig = px.treemap(
    df_tree_fpe,
    ids="id",
    names="nom",
    parents="parent_id",
    color="nature",
    title=f"Hiérarchie DILA — FPE + institutions ({len(df_tree_fpe):,} nœuds)",
    hover_data=["siren", "siret", "slug_1"],
)
fig.show(renderer="iframe")
```

> **Les données de l'annuaire des services public de la DILA permet de reproduire la notion de hierarchie au sein des organismes de la FPE**

```python
# Nœuds racines = ceux qui n'ont pas de parent dans df_dila_full
racines = df_dila_full[df_dila_full["parent_id"] == ""].copy()

print(f"Nombre de racines : {len(racines)}")
print(f"Racines sans SIREN ni SIRET : {(~racines['siren'].apply(has_val) & ~racines['siret'].apply(has_val)).sum()}")
print(f"Soit : {(~racines['siren'].apply(has_val) & ~racines['siret'].apply(has_val)).mean():.0%}")

```

```python
# ── Identifier l'id du nœud référent (le plus fin avec SIREN ou SIRET) ──
def get_referent_id_finest(node_id):
    """Retourne l'id du nœud le plus fin (= le plus proche de la feuille) avec SIREN ou SIRET."""
    current = node_id
    for _ in range(20):
        if has_val(id_to_siren.get(current)) or has_val(id_to_siret.get(current)):
            return current  # premier trouvé en remontant = le plus fin
        parent = id_to_parent.get(current, "")
        if not parent:
            break
        current = parent
    return None  # aucun SIREN/SIRET sur le chemin

# Exclure la territoriale
df_hors_terr_full = df_dila_full[
    df_dila_full["nature"] != "Territorial (région/dép.)"
].copy()
#df_hors_terr_full = df_dila_full.copy()

df_hors_terr_full["referent_id"] = df_hors_terr_full["id"].apply(get_referent_id_finest)

# ── Agrégation correcte ───────────────────────────────────────────────────
# Cas 1 : nœuds avec référent → on ne garde QUE la ligne où id == referent_id
referents_uniques  = set(df_hors_terr_full["referent_id"].dropna().unique())

# Cas 2 : nœuds sans référent (aucun SIREN/SIRET sur tout le chemin)
sans_referent_ids  = set(df_hors_terr_full[df_hors_terr_full["referent_id"].isna()]["id"])

# On filtre df_flat_sorted sur les ids hors territorial d'abord,
# puis on ne garde que les référents uniques + les orphelins
ids_hors_terr = set(df_hors_terr_full["id"])
ids_a_garder  = (referents_uniques | sans_referent_ids) & ids_hors_terr

df_flat_agg = df_flat_sorted[df_flat_sorted["id"].isin(ids_a_garder)].copy()

print(f"Avant agrégation (hors territorial) : {df_flat_sorted[df_flat_sorted['id'].isin(ids_hors_terr)].shape[0]:,} lignes")
print(f"Après agrégation                     : {len(df_flat_agg):,} lignes")
print(f"  dont référents uniques (avec SIREN/SIRET) : {len(referents_uniques):,}")
print(f"  dont orphelins (sans SIREN/SIRET)         : {len(sans_referent_ids):,}")
print(f"  dont avec siren_effectif renseigné        : {df_flat_agg['siren_effectif'].notna().sum():,}")

df_flat_agg.to_csv("data/dila_flat_hierarchy.csv", index=False, encoding="utf-8-sig")

```

> **Mais les SIRET / SIREN sont souvent manquants, et ce n'est pas seulement du à une granularité trop fine (exemple : bureaux).**


> **Le taux de complétude des siret / siren nécessite une API externe**


> **Si on s'appuie sur les données de la DILA pour la FPE: il sera nessaire de mettre une heuristique pour couper le référenciel au niveau des feuilles (bureaux etc.)**


### 2.4 Comparaison des champs d'intéret

```python
import httpx
import time

RECHERCHE_API = "https://recherche-entreprises.api.gouv.fr/search"

def fetch_siren_by_name(nom: str) -> tuple[str | None, str | None]:
    """Retourne (siren, siret_siege) depuis l'API recherche-entreprises."""
    try:
        resp = httpx.get(
            RECHERCHE_API,
            params={
                "q": nom,
                "categorie_juridique": "7120",  # organismes d'État
                "per_page": 1,
            },
            timeout=10,
        )
        results = resp.json().get("results", [])
        if results:
            r = results[0]
            return r.get("siren"), r.get("siege", {}).get("siret")
    except Exception:
        pass
    return None, None

# Enrichir uniquement les organismes sans siren_effectif
sans_siren = df_hors_terr[
    df_hors_terr["siren_effectif"].isna() & df_hors_terr["siret_effectif"].isna()
].copy()

sirens, sirets = [], []
for nom in sans_siren["nom"]:
    s, st = fetch_siren_by_name(nom)
    sirens.append(s)
    sirets.append(st)
    time.sleep(0.1)  # politesse API

sans_siren["siren_api"] = sirens
sans_siren["siret_api"] = sirets

print(f"Enrichis via API : {sans_siren['siren_api'].notna().sum()} / {len(sans_siren)}")
sans_siren[["nom", "nature", "siren", "siren_effectif", "siren_api", "siret_api"]].head(20)

```
