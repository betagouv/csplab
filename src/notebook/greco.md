```python
import pandas as pd

# Import du CSV
df = pd.read_csv('GRECO_export_20251118.csv', sep=';')

# Affichage des informations de base
print(f"Shape: {df.shape}")
print(f"Colonnes: {list(df.columns)}")
df.head()
df.columns
```

# Nettoyage


## Filtrage

```python
import polars as pl
import pelage as plg

def print_filter_stats(df_before, df_after, filter_name):
    """Print statistics about filtering step."""
    before = len(df_before)
    after = len(df_after)
    lost = before - after
    pct_lost = (lost / before * 100) if before > 0 else 0
    print(f"{filter_name}: {before} → {after} (-{lost}, -{pct_lost:.1f}%)")

df = pl.read_csv('GRECO_export_20251118.csv', separator=';')
print(f"Données initiales: {len(df)} lignes, {len(df.columns)} colonnes")

# Filtre Statut : VALIDE
df_before = df
df = df.filter(pl.col('Statut') == "VALIDE")
print_filter_stats(df_before, df, "Filtre Statut = VALIDE")


df_before = df
df = df.filter(pl.col('Année de référence') > 2024)
print_filter_stats(df_before, df, "Filtre année > 2024")
print("---------------------------------------------------------- df length:", len(df))

required_cols = ['N° NOR', 'Année de référence', 'Corps', 'Catégorie']

for col in required_cols:  # Exclut 'Date de première épreuve'
    df_before = df
    df = df.filter(pl.col(col).is_not_null())
    print_filter_stats(df_before, df, f"Filtre {col} non-null")
```

```python
list(df['Ministère'].unique())
```

```python
df.write_csv("greco_after2025.csv", separator=";")
```

## Dédoublonnage

```python
# Step 1: create concours_id_temp
df = df.with_columns([
    pl.when(pl.col('N° NOR de référence').is_not_null())
    .then(pl.col('N° NOR de référence'))
    .otherwise(pl.col('N° NOR'))
    .alias('concours_id_temp')
])

# Step 2: Identify concours_id with several corps
multi_corps_ids = (
    df.group_by('concours_id_temp')
    .agg(pl.col('Corps').n_unique().alias('nb_corps'))
    .filter(pl.col('nb_corps') > 1)
    .select('concours_id_temp')
    .to_series()
    .to_list()
)

# Step 3: create concours_id final
df = df.with_columns([
    pl.when(pl.col('concours_id_temp').is_in(multi_corps_ids))
    .then(pl.col('N° NOR'))  # use N° NOR if several corps
    .otherwise(pl.col('concours_id_temp'))
    .alias('concours_id')
]).drop('concours_id_temp')

df.head()
```

```python
def extract_nor_sort_key(nor_value: str) -> int:
    """Extract sorting key from NOR for chronological ordering."""
    if not nor_value or len(nor_value) != 12:
        return 0
    try:
        # Extract year (positions 4-5) and sequence (positions 6-10)
        year = int(nor_value[4:6])
        sequence = int(nor_value[6:11])
        return year * 100000 + sequence
    except (ValueError, IndexError):
        return 0

df = df.with_columns([
    pl.col('N° NOR').map_elements(extract_nor_sort_key, return_dtype=pl.Int64).alias('nor_sort_key')
])

df_dedup = (
    df.sort('nor_sort_key', descending=True)
    .group_by('concours_id')
    .agg([
        # Garder la première ligne (NOR le plus récent) pour tous les autres champs
        pl.all().first(),
        # Agréger tous les NOR du concours
        pl.col('N° NOR').alias('all_nors_in_concours')
    ])
    .drop('nor_sort_key')
)
```

## Sélection des variables d'intéret

```python
df_final = df_dedup.select([
    'concours_id', 'Ministère', 'Catégorie', 'Corps', 'Grade',
    'all_nors_in_concours', 'Nb postes total', 'Date de première épreuve',
    # Ajouter toutes les colonnes de modalités d'accès
    'Externe', 'Interne', 'Troisieme Concours', 'Unique',
    'Examen professionnel', 'Sans concours externe', 'Pacte',
    'Sélection professionnelle', 'Concours spécial', 'Concours réservé',
    'Sans concours interne réservé', 'Examen professionnalisé réservé',
    'Interne exceptionnel', 'Apprenti BOETH', 'Promotion BOETH', 'Autres'
])

access_modality_cols = [
    'Externe', 'Interne', 'Troisieme Concours', 'Unique',
    'Examen professionnel', 'Sans concours externe', 'Pacte',
    'Sélection professionnelle', 'Concours spécial', 'Concours réservé',
    'Sans concours interne réservé', 'Examen professionnalisé réservé',
    'Interne exceptionnel', 'Apprenti BOETH', 'Promotion BOETH', 'Autres'
]

df_final = df_final.with_columns([
    pl.concat_list([
        pl.when(
            (pl.col(col).is_not_null()) &
            (pl.col(col).cast(pl.Utf8) != "0") &
            (pl.col(col).cast(pl.Utf8) != "") &
            (pl.col(col).cast(pl.Utf8) != "null")
        )
        .then(pl.lit(col))
        .otherwise(None)
        for col in access_modality_cols
    ]).list.drop_nulls().alias('mod_access')
])

df_final = df_final.select([
    'concours_id', 'Ministère', 'Catégorie', 'Corps', 'Grade',
    'all_nors_in_concours', 'Nb postes total', 'Date de première épreuve',
    'mod_access'
])

df_final.head()
```

```python
df_final
```

```python

```
