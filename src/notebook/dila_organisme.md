## Note de faisabilité — API DILA (Annuaire des services publics)

<!-- #region -->
### 1. Données disponibles

L'API DILA expose un annuaire public de **~94 000 services publics français**, sans authentification, exportable en CSV. Les champs d'intérêt sont :

| Champ | Utilité |
|---|---|
| `id` (UUID) | Identifiant unique |
| `nom` | Matching sémantique |
| `type_organisme` + `categorie` | Qualification de l'entité |
| `siren` / `siret` | Jonction avec le référentiel légal |
| `adresse` (JSON) → `longitude`, `latitude` | Géolocalisation |
| `url_service_public` | Distinction FPT vs FPE |
| `date_creation`, `date_modification` | Fraîcheur |
| `hierarchie` → `parent_id` reconstruit | Structure hiérarchique |

---

### 2. Convergence avec la structure CSP

La structure DILA **converge bien** avec le modèle Entité de CSP sur les points suivants :

| Besoin fonctionnel | Champ DILA | Champ TS (`df_orgs`) | Alignement |
|---|---|---|---|
| **Identifiant unique** | `id` (UUID) | `code` (interne TS) | ⚠️ Hétérogènes — nécessite une table de correspondance |
| **Identifiant métier** | `siren` / `siret` | `clientCode` (code ministériel) | ⚠️ Natures différentes : SIREN vs code RH, ⚠️ DILA nécessite une autre API comme https://recherche-entreprises.api.gouv.fr/search |
| **Nom / libellé** | `nom` | `label` | ✅ Équivalents — matching sémantique possible |
| **Hiérarchie parent** | `hierarchie` → `parent_id` reconstruit | `parentCode` | ✅ Même concept, bien aligné |
| **Type d'organisme** | `type_organisme` + `categorie` | `type` + `parentType` | ⚠️ Granularités différentes |
| **Localisation** | `longitude` / `latitude` | `geolocation` dans details | ✅ Même concept, bien aligné, ⚠️ 60% complet chez TS|


> **Clé de jonction possible :**
> 1. `nom` (DILA) ↔ `label` (TS) — matching sémantique / flou
> 2. `parent_id` reconstruit (DILA) ↔ `parentCode` (TS) — pour valider la cohérence hiérarchique
> 3. ajout matching geographique (97% de complétude DILA FPE et 60% des organismes du référeciel TS)


### 3. Couverture pour nos types d'entités cibles

- **FPE (ministères, établissements publics)** → catégorie `SI` — ✅ bien couverte, hiérarchie reconstituable
- **FPT (collectivités)** → identifiable via `url_service_public` et `slug` — ✅ présente mais volumineuse (~majorité des 94 000 entrées)
- **FPH (hôpitaux)** → absent
- **Ambassades / international** → ✅ slug `ambassades` identifié

---

### 4. Fraîcheur des données

- Données mises à jour régulièrement par la DILA (date de modification disponible par enregistrement)
- 75% des données ont moins d'un an, TS a un champ `active`
- **Mécanisme de mise à jour : aucun webhook ni abonnement** — il faut **interroger l'API périodiquement** (export CSV complet ou requêtes filtrées)
- L'API expose une date `data_processed` par dataset permettant de détecter les mises à jour

---

### 5. Authentification

**Aucune authentification requise.** L'API est publique, accessible sans clé ni token.

---

### 6. Abonnement vs polling

| Mécanisme | Disponible ? |
|---|---|
| Webhooks / événements | ❌ Non |
| Flux de changements (delta) | ❌ Non |
| Export CSV complet | ✅ Oui |
| Filtres par date de modification | ✅ Possible via paramètres de requête |

→ **Stratégie nécessaire : import périodique** (ex. hebdomadaire) avec détection des changements par comparaison de `date_modification`.

---

### 7. Recommandation

**→ Import initial ponctuel + synchronisation périodique par polling**

- **Import initial** : export CSV complet, filtrage sur `categorie == "SI"` (FPE) + reconstruction de la hiérarchie
- **Synchronisation** : polling hebdomadaire, mise à jour des enregistrements dont `date_modification` a changé
- **Matching avec TS** : par nom (`nom` ↔ `label`) avec seuil de similarité sémantique, à valider manuellement sur un échantillon

---

### 8. Risques et limites

| Risque | Niveau | Mitigation |
|---|---|---|
| Pas de mécanisme push | 🟡 Moyen | Polling régulier sur `date_modification` |
| SIREN/SIRET souvent absents sur les feuilles (bureaux) | 🟡 Moyen | Enrichissement via API recherche-entreprises |
| Pas de champ `actif/inactif` | 🟠 Fort | Heuristique sur `date_modification` ancienne |
| Matching DILA ↔ TS par nom uniquement | 🟠 Fort | Validation humaine sur les cas ambigus |
| Volume FPT très élevé (>80% des entrées), absence de la FPH | 🟡 Moyen | Filtrage strict par `categorie` |
| Qualité variable de la géolocalisation | 🟡 Moyen | Complétude à mesurer (taux partiel constaté côté TS) |
<!-- #endregion -->

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

```python
df_dila_full["categorie"].value_counts()
```

```python
df_dila_full["type_organisme"].value_counts()
```

```python
pd.crosstab(
    df_dila_full["type_organisme"],
    df_dila_full["categorie"],
    margins=True,
    margins_name="Total"
)
```

## 2. La structure proposée converge-t-elle avec la structure des entités dans CSP ?


### 2.1 Analyse de la structure du référenciel Organisation de TS

```python
import httpx
import os

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
print(df_orgs.columns)
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
fig.show(renderer="notebook_connected")
```

```python
# ── Taux de complétude géolocalisation — Talentsoft (organismes actifs) ───────
# Note : df_details est construit sur df_orgs[active==True], donc tous les
#        enregistrements sont déjà des organismes actifs.

def extract_geo_ts(g):
    if isinstance(g, dict):
        try:
            lat = float(g.get("latitude") or "nan")
            lon = float(g.get("longitude") or "nan")
            return (
                lat if not pd.isna(lat) else None,
                lon if not pd.isna(lon) else None,
            )
        except (ValueError, TypeError):
            pass
    return None, None

geo_ts = df_details["geolocation"].apply(extract_geo_ts)
df_details["geo_lat"] = geo_ts.apply(lambda x: x[0])
df_details["geo_lon"] = geo_ts.apply(lambda x: x[1])

n = len(df_details)
has_geo = df_details["geo_lat"].notna() & df_details["geo_lon"].notna()
n_geo   = has_geo.sum()

print(f"[TS — actifs] Avec géolocalisation : {n_geo:,} / {n:,}  ({n_geo/n:.1%})")
print(f"[TS — actifs] Sans géolocalisation : {n - n_geo:,} / {n:,}  ({(n - n_geo)/n:.1%})")
```

> ### Conclusion : dans le référenciel des organismes de TS, la notion parent / enfant (hierarchique) est centrale pour la FPE.


### 2.2 Analyse de la structure du référenciel Organisation de TS utilisée en pratique

```python
import re
from sqlalchemy import create_engine
import os

raw_url = os.getenv("WEB_DATABASE_URL", "postgresql+psycopg2://web:pass@localhost:5432/web")

# Normalise le schéma vers psycopg2 (psql://, postgres://, postgresql:// → postgresql+psycopg2://)
url = re.sub(r'^(?:postgresql|postgres|psql)(?:\+\w+)?://', 'postgresql+psycopg2://', raw_url)

engine = create_engine(url)
```

#### Organismes depuis la BDD

```python
import pandas as pd

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
    values="offer_count",
    hover_data=["clientCode"],
)
fig.show(renderer="notebook_connected")
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
fig.show(renderer="notebook_connected")
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
df_viz_all = df_dila_full[df_dila_full["parent_id"] != ""].copy()

parent_ids_manquants = set(df_viz_all["parent_id"]) - set(df_viz_all["id"])
df_parents = df_dila_full[df_dila_full["id"].isin(parent_ids_manquants)]
df_tree_all = pd.concat([df_viz_all, df_parents]).drop_duplicates("id")

fig = px.treemap(
    df_tree_all,
    ids="id", names="nom", parents="parent_id",
    title=f"Hiérarchie DILA all ({len(df_tree_all):,} nœuds)",
    hover_data=["siren", "siret"],
)
fig.show(renderer="notebook_connected")
```

```python
df_dila_fpe = df_dila_full[df_dila_full["categorie"] == "SI"]
df_viz_fpe  = df_dila_fpe[df_dila_fpe["parent_id"] != ""].copy()

# ← chercher dans df_dila_FULL, pas df_dila_fpe
parent_ids_manquants = set(df_viz_fpe["parent_id"]) - set(df_viz_fpe["id"])
df_parents = df_dila_full[df_dila_full["id"].isin(parent_ids_manquants)]
df_tree_fpe = pd.concat([df_viz_fpe, df_parents]).drop_duplicates("id")

# Sécurité : neutraliser les parent_id qui restent introuvables
ids_valides = set(df_tree_fpe["id"])
df_tree_fpe["parent_id"] = df_tree_fpe["parent_id"].where(
    df_tree_fpe["parent_id"].isin(ids_valides), other=""
)

print(f"Nœuds: {len(df_tree_fpe):,}")

fig = px.treemap(
    df_tree_fpe,
    ids="id", names="nom", parents="parent_id",
    title=f"Hiérarchie DILA FPE ({len(df_tree_fpe):,} nœuds)",
    hover_data=["siren", "siret"],
)
fig.show(renderer="notebook_connected")
```

> **Les données de l'annuaire des services public de la DILA permet de reproduire la notion de hierarchie au sein des organismes de la FPE**

```python
# ── Dicts de lookup sur le FULL (indispensable pour traverser toute la hiérarchie) ──
id_to_siren  = df_dila_full.set_index("id")["siren"].to_dict()
id_to_siret  = df_dila_full.set_index("id")["siret"].to_dict()
id_to_parent = df_dila_full.set_index("id")["parent_id"].to_dict()

def has_val(val) -> bool:
    return pd.notna(val) and str(val).strip() not in ("", "nan")

# ── Identifier l'id du nœud référent (le plus fin avec SIREN ou SIRET) ──
def get_referent_id_finest(node_id):
    current = node_id
    for _ in range(20):
        if has_val(id_to_siren.get(current)) or has_val(id_to_siret.get(current)):
            return current
        parent = id_to_parent.get(current, "")
        if not parent:
            break
        current = parent
    return None

# ── Partir de df_dila_fpe (catégorie SI) ──────────────────────────────────────
df_fpe_work = df_dila_fpe.copy()
df_fpe_work["referent_id"] = df_fpe_work["id"].apply(get_referent_id_finest)

# ── Agrégation ───────────────────────────────────────────────────────────────
# Cas 1 : nœuds avec référent → on ne garde QUE la ligne où id == referent_id
referents_uniques = set(df_fpe_work["referent_id"].dropna().unique())

# Cas 2 : nœuds sans référent (aucun SIREN/SIRET sur tout le chemin)
sans_referent_ids = set(df_fpe_work[df_fpe_work["referent_id"].isna()]["id"])

# On ne garde que les référents uniques + les orphelins, dans les ids SI
ids_fpe = set(df_fpe_work["id"])
ids_a_garder = (referents_uniques | sans_referent_ids) & ids_fpe

df_flat_agg = df_dila_fpe[df_dila_fpe["id"].isin(ids_a_garder)].copy()

print(f"Avant agrégation (catégorie SI) : {len(df_dila_fpe):,} lignes")
print(f"Après agrégation                : {len(df_flat_agg):,} lignes")
print(f"  dont référents uniques (avec SIREN/SIRET) : {len(referents_uniques & ids_fpe):,}")
print(f"  dont orphelins (sans SIREN/SIRET)         : {len(sans_referent_ids):,}")
print(f"  dont avec siren renseigné                 : {df_flat_agg['siren'].notna().sum():,}")

df_flat_agg.to_csv("data/dila_flat_fpe.csv", index=False, encoding="utf-8-sig")
```

> **Mais les SIRET / SIREN sont souvent manquants, et ce n'est pas seulement du à une granularité trop fine (exemple : bureaux).**


> **Le taux de complétude des siret / siren nécessite une API externe**

```python
# ── Treemap de df_flat_agg (référents SI agrégés) ────────────────────────────

# Récupérer les parents manquants depuis df_dila_full
parent_ids_manquants = set(df_flat_agg["parent_id"]) - {""} - set(df_flat_agg["id"])
df_parents_tree = df_dila_full[df_dila_full["id"].isin(parent_ids_manquants)]
df_tree_agg = pd.concat([df_flat_agg, df_parents_tree]).drop_duplicates("id").copy()

# Neutraliser les parent_id encore fantômes (parents de parents hors périmètre)
ids_valides = set(df_tree_agg["id"])
df_tree_agg["parent_id"] = df_tree_agg["parent_id"].where(
    df_tree_agg["parent_id"].isin(ids_valides), other=""
)

print(f"Nœuds dans le treemap : {len(df_tree_agg):,}")

fig = px.treemap(
    df_tree_agg,
    ids="id",
    names="nom",
    parents="parent_id",
    title=f"Hiérarchie DILA — Référents FPE/SI agrégés ({len(df_flat_agg):,} nœuds)",
    hover_data=["siren", "siret"],
)
fig.show(renderer="notebook_connected")
```

> **Si on s'appuie sur les données de la DILA pour la FPE: il sera aussi necessaire de mettre en place une heuristique pour couper le référenciel au niveau des feuilles (bureaux etc.)**

```python
import json

def extract_geo(adresse_raw):
    if not isinstance(adresse_raw, str):
        return None, None
    try:
        adresses = json.loads(adresse_raw)
        for adr in adresses:
            lon = adr.get("longitude", "").strip()
            lat = adr.get("latitude", "").strip()
            if lon and lat:
                return float(lon), float(lat)
    except Exception:
        pass
    return None, None

# Extraire
geo = df_flat_agg["adresse"].apply(extract_geo)
df_flat_agg["geo_lon"] = geo.apply(lambda x: x[0])
df_flat_agg["geo_lat"] = geo.apply(lambda x: x[1])

# ── Taux de complétude ────────────────────────────────────────────────────────
n = len(df_flat_agg)
has_geo = df_flat_agg["geo_lon"].notna() & df_flat_agg["geo_lat"].notna()
n_geo   = has_geo.sum()

print(f"Avec géolocalisation : {n_geo:,} / {n:,}  ({n_geo/n:.1%})")
print(f"Sans géolocalisation : {n - n_geo:,} / {n:,}  ({(n - n_geo)/n:.1%})")

```

```python

# ── Fraîcheur des données DILA — df_flat_agg (FPE / catégorie SI) ─────────────
df_flat_agg["date_modification"] = pd.to_datetime(df_flat_agg["date_modification"], errors="coerce")
df_flat_agg["date_creation"]     = pd.to_datetime(df_flat_agg["date_creation"], errors="coerce")

today = pd.Timestamp.now().normalize()
n     = len(df_flat_agg)
age   = (today - df_flat_agg["date_modification"]).dt.days

# 1. Complétude des dates
pd.DataFrame({
    "champ":        ["date_creation", "date_modification"],
    "renseignés":   [df_flat_agg["date_creation"].notna().sum(),
                     df_flat_agg["date_modification"].notna().sum()],
    "total":        [n, n],
    "complétude":   [f"{df_flat_agg['date_creation'].notna().mean():.1%}",
                     f"{df_flat_agg['date_modification'].notna().mean():.1%}"],
})
```

```python
pd.DataFrame([
    {
        "fenêtre": f"{j} jours",
        "organismes": (df_flat_agg["date_modification"] >= today - pd.Timedelta(days=j)).sum(),
        "% du total": f"{(df_flat_agg['date_modification'] >= today - pd.Timedelta(days=j)).mean():.1%}",
    }
    for j in [30, 90, 180, 365]
])
```

```python
(
    df_flat_agg["date_modification"]
    .dt.year
    .value_counts()
    .sort_index(ascending=False)
    .rename_axis("année")
    .reset_index(name="nb_organismes")
    .assign(pct=lambda d: (d["nb_organismes"] / n).map("{:.1%}".format))
)

```

```python
# ── Couverture FPH dans df_dila_full ─────────────────────────────────────────

# 1. Explorer le croisement categorie × type_organisme pour repérer la FPH
pd.crosstab(
    df_dila_full["categorie"],
    df_dila_full["type_organisme"],
    margins=True,
    margins_name="Total"
).sort_values("Total", ascending=False)
```

```python
# 2. Identifier les valeurs de type_organisme qui semblent relever de la FPH
fph_keywords = ["hôpital", "hopital", "chu", "chru", "chp", "ehpad", "clinique",
                "soin", "santé", "médico", "psychiatr", "maternité"]

mask_fph = df_dila_full["nom"].str.lower().str.contains(
    "|".join(fph_keywords), na=False
)

df_fph = df_dila_full[mask_fph].copy()
print(f"Organismes FPH identifiés : {len(df_fph):,}")

# Répartition par type_organisme
df_fph["type_organisme"].value_counts().reset_index()
```

```python
# 3. Couverture : % avec siren/siret, géolocalisation
n_fph = len(df_fph)

pd.DataFrame([
    {"indicateur": "Total FPH identifiés",            "valeur": f"{n_fph:,}",          "taux": "—"},
    {"indicateur": "Avec SIREN",                       "valeur": f"{df_fph['siren'].notna().sum():,}", "taux": f"{df_fph['siren'].notna().mean():.1%}"},
    {"indicateur": "Avec SIRET",                       "valeur": f"{df_fph['siret'].notna().sum():,}", "taux": f"{df_fph['siret'].notna().mean():.1%}"},
    {"indicateur": "Avec parent_id (dans hiérarchie)", "valeur": f"{(df_fph['parent_id'] != '').sum():,}", "taux": f"{(df_fph['parent_id'] != '').mean():.1%}"},
])
```
