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

## Une observation = un numéro NOR

```python
df
```

```python
df[df['Corps'].isna() == True]
```

```python
len(df['N° NOR'].unique())
len(df)
```

```python
nb_corps = len(df['Corps'].unique())
nb_grades = len(df['Grade'].unique())
print(f"Nombre de corps: {nb_corps}")
print(f"Nombre de grades: {nb_grades}")
```

```python
combinaisons = df[['Corps', 'Grade','Ministère','Date de première épreuve']].value_counts()
nb_uniques = len(combinaisons)
print(f"Nombre de combinaisons uniques: {nb_uniques}")
```

```python
df['Année de référence'].unique()
```

```python
# Identifier les combinaisons dupliquées
combinaisons_dupliquees = combinaisons[combinaisons > 1].index

# Créer un masque pour filtrer le DataFrame original
mask = df.set_index(['Corps', 'Grade','Ministère','Date de première épreuve']).index.isin(combinaisons_dupliquees)

# Afficher toutes les lignes concernées
lignes_dupliquees = df[mask].sort_values(['Corps', 'Grade','Ministère','Date de première épreuve'])
print(f"Nombre total de lignes avec doublons: {len(lignes_dupliquees)}")
lignes_dupliquees
```

```python
df_indexed = df.set_index('N° NOR')
df_indexed.loc['MENH2435486A']
```

```python
df_indexed.loc['MENH2506115A']
```

# Clean Concours

```python
df_clean = df[df['Année de référence'] > 2024 && df['Date de première épreuve'] > ]
```

```python
import pandas as pd
from datetime import datetime

# Convertir la colonne date en format datetime
df['Date de première épreuve'] = pd.to_datetime(df['Date de première épreuve'], format='%d/%m/%Y', errors='coerce')

# Date d'aujourd'hui
aujourd_hui = datetime.now()

# Filtrage corrigé (& au lieu de &&)
df_clean = df[
    (df['Année de référence'] > 2024) &
    (df['Date de première épreuve'] > aujourd_hui)
]

print(f"Données originales: {len(df)} lignes")
print(f"Données filtrées: {len(df_clean)} lignes")
print(f"Date de référence: {aujourd_hui.strftime('%d/%m/%Y')}")

```

```python
df_clean
```

```python
df['Examen professionnel'].unique()
```

```python
df['Unique'].unique()
```

```python
df['Pacte'].unique()
```

```python
df['Autres'].unique()
```

```python
df['Promotion BOETH'].unique()
```

```python
df['Apprenti BOETH'].unique()
```

```python
df['Déconcentré'].unique()
```

```python
df[df['Ministère']==""]
```

```python

```
