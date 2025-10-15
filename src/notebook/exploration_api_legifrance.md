---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.3
kernelspec:
  name: csplab-base
  display_name: CSPLab Base (pandas, numpy, matplotlib)
  language: python
---

```{code-cell} ipython3
!uv add pylegifrance
!uv add python-dotenv
!uv add qgrid
```

```{code-cell} ipython3
from dotenv import load_dotenv
from pylegifrance import ApiConfig
import os

load_dotenv()

try:
    config = ApiConfig.from_env()
    print(config.client_id)
    print("✅ Configuration chargée depuis les variables d'environnement")
    print(f"Client ID présent: {'✅' if config.client_id else '❌'}")
except ValueError as e:
    print(f"❌ Erreur: {e}")
```

```{code-cell} ipython3
import pandas as pd
from pylegifrance import LegifranceClient
from pylegifrance.fonds.loda import Loda
from pylegifrance.models.loda.search import SearchRequest

def get_all_concours_fonction_publique(client: LegifranceClient, annee: str):
    """
    Récupère TOUS les concours de la fonction publique pour une année
    avec pagination automatique
    """
    loda = Loda(client)
    all_results = []
    page = 1

    print(f"🔍 Recherche de tous les concours {annee}...")

    while True:
        print(f"📄 Page {page}...", end=" ")

        search_request = SearchRequest(
            search=f"concours {annee}",
            natures=["ARRETE", "AVIS", "DECISION"],
            page_number=page,
            page_size=100
        )

        try:
            results = loda.search(search_request)

            if not results:
                print("✅ Terminé (aucun résultat)")
                break

            print(f"({len(results)} résultats)")
            all_results.extend(results)

            if len(results) < 100:
                print("✅ Terminé (dernière page)")
                break

            page += 1

            if page > 50:
                print("⚠️ Limite de sécurité atteinte")
                break

        except Exception as e:
            print(f"❌ Erreur page {page}: {e}")
            break

    print(f"\n📊 Total récupéré: {len(all_results)} concours")
    return all_results
```

```{code-cell} ipython3
def results_to_complete_dataframe(results):
    """Accède aux propriétés de TexteLoda, extrait date et ministère avec mapping correct"""
    if not results:
        return pd.DataFrame()

    # Mapping des codes ministères (3 premières lettres du NOR)
def results_to_complete_dataframe(results):
    """Accède aux propriétés de TexteLoda, extrait date et ministère avec mapping complet"""
    if not results:
        return pd.DataFrame()

    # Mapping complet des codes ministères (3 premières lettres du NOR)
    ministeres = {
        'ARM': 'Ministère des Armées',
        'MEN': 'Ministère de l\'Éducation nationale, jeunesse et sports',
        'ECO': 'Ministère de l\'Économie, finances et relance',
        'INT': 'Ministère de l\'Intérieur et Outre-mer',
        'JUS': 'Ministère de la Justice',
        'AGR': 'Ministère de l\'Agriculture et souveraineté alimentaire',
        'MIC': 'Ministère de la Culture',
        'ESR': 'Ministère de l\'Enseignement supérieur, recherche et innovation',
        'TRE': 'Ministère de la Transition écologique et cohésion des territoires',
        'IOM': 'Ministère de l\'Outre-mer',
        'SSA': 'Ministère des Solidarités, santé et personnes handicapées',
        'TSS': 'Ministère du Travail, emploi et insertion',
        'TFP': 'Ministère de la Transformation et fonction publique',
        'EAE': 'Ministère de l\'Europe et des Affaires étrangères',
        'TEC': 'Ministère de la Transition écologique',
        'PRM': 'Services du Premier Ministre',
        'ATD': 'Ministère de la Cohésion des territoires',
        'SPO': 'Ministère des Sports et des Jeux olympiques',
        'CPA': 'Ministère de l\'Action et des Comptes publics',
        'SPR': 'Ministère des Solidarités',
        'APF': 'Agence publique',
        'MER': 'Ministère de la Mer',
        'TER': 'Ministère de la Transition écologique (territoires)',
        'CCP': 'Collectivités et collectivités publiques',
        'PTD': 'Ministère de la Fonction publique (patrimoine et technique)',
        'TRA': 'Ministère des Transports',
        'DEV': 'Ministère du Développement durable',
        'BCP': 'Ministère du Budget et Comptes publics',
        'APH': 'Agence publique hospitalière',
        'MSA': 'Mutualité Sociale Agricole',
        'DEF': 'Ministère de la Défense',
        'FCP': 'Finances, Comptes publics',
        'IOC': 'Institution culturelle ou sportive',
        'VIL': 'Ville, collectivités territoriales',
        'EFI': 'Ministère de l\'Économie Financière',
        'CPT': 'Ministère de la Cohésion territoriale',
        'FAM': 'Ministère des Familles',
        'ENE': 'Ministère de l\'Énergie'
    }

    data = []
    for result in results:
        # Extraire la date depuis l'ID
        date_from_id = None
        if result.id and '_' in result.id:
            try:
                date_part = result.id.split('_')[1]
                day, month, year = date_part.split('-')
                date_from_id = f"{year}-{month}-{day}"
            except:
                date_from_id = None

        # Extraire le ministère depuis le NOR (3 premières lettres)
        ministere = None
        if result.nor:
            code_ministere = str(result.nor)[:3].upper()
            ministere = ministeres.get(code_ministere, f"Autre ({code_ministere})")

        row = {
            'id': result.id,
            'titre': result.titre,
            'cid': str(result.cid) if result.cid else None,
            'nor': str(result.nor) if result.nor else None,
            'date_publication': result.date_publication or date_from_id,
            'etat': result.etat,
            'ministere': ministere
        }
        data.append(row)

    return pd.DataFrame(data)


    data = []
    for result in results:
        # Extraire la date depuis l'ID
        date_from_id = None
        if result.id and '_' in result.id:
            try:
                date_part = result.id.split('_')[1]
                day, month, year = date_part.split('-')
                date_from_id = f"{year}-{month}-{day}"
            except:
                date_from_id = None

        # Extraire le ministère depuis le NOR (3 premières lettres)
        ministere = None
        if result.nor:
            code_ministere = str(result.nor)[:3].upper()
            ministere = ministeres.get(code_ministere, f"Autre ({code_ministere})")

        row = {
            'id': result.id,
            'titre': result.titre,
            'cid': str(result.cid) if result.cid else None,
            'nor': str(result.nor) if result.nor else None,
            'date_publication': result.date_publication or date_from_id,
            'etat': result.etat,
            'ministere': ministere
        }
        data.append(row)

    return pd.DataFrame(data)
```

```{code-cell} ipython3
# API calls
client = LegifranceClient()

all_years = []

for year in range(2020, 2025 + 1):
    all_years.append(get_all_concours_fonction_publique(client, year))
```

```{code-cell} ipython3
all_df = []
for year in all_years:
    all_df.append(results_to_complete_dataframe(year))
```

```{code-cell} ipython3
df_consolidated = pd.concat(all_df, ignore_index=True)
```

```{code-cell} ipython3
df_consolidated.head()
```

```{code-cell} ipython3
prefixes_3 = df_consolidated['nor'].dropna().apply(lambda x: str(x)[:3]).value_counts()
print("Préfixes 3 lettres:")
print(prefixes_3[:10])
```

```{code-cell} ipython3
def analyze_coverage(df):
    keywords = ['hospitalier', 'hôpital', 'CHU', 'CHR', 'APHP', 'santé']

    concours = df[df['titre'].str.contains('|'.join(keywords), case=False, na=False)]

    print(f"Concours trouvés: {len(concours)}")
    print("Échantillon:")
    print(concours[['titre', 'ministere']].head(10))

    return concours

results = analyze_coverage(df_consolidated)
```

```{code-cell} ipython3

```
