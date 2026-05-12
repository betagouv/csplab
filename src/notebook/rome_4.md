---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.1
  kernelspec:
    display_name: CSPLab Base (pandas, numpy, matplotlib)
    language: python
    name: csplab-base
---

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
FRANCE_TRAVAIL_CLIENT_ID = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
FRANCE_TRAVAIL_CLIENT_SECRET = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")

```

```python
import requests
import json

def get_token():
    response = requests.post(
        "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire",
        data={
            'grant_type': 'client_credentials',
            'client_id': FRANCE_TRAVAIL_CLIENT_ID,
            'client_secret': FRANCE_TRAVAIL_CLIENT_SECRET,
            'scope': 'nomenclatureRome api_rome-competencesv1'
        }
    )
    if response.status_code != 200:
        print(f"Erreur token: {response.status_code} - {response.text}")
        return None
    return response.json()['access_token']

def get_competences():
    token = get_token()
    if not token:
        return None

    params = {
        'champs': 'libelle,code,@competencedetaillee(macrocompetence(libelle,souscategorie)),@macrocompetence(souscategorie),@savoir(categoriesavoir(libelle,code))'
    }

    response = requests.get(
        "https://api.francetravail.io/partenaire/rome-competences/v1/competences/competence",
        headers={'Authorization': f'Bearer {token}'},
        params=params
    )
    if response.status_code != 200:
        print(f"Erreur API: {response.status_code} - {response.text}")
        return None
    return response.json()

def mapper_type_competence(comp):
    comp_type = comp.get('type', '')

    if comp_type == 'SAVOIR':
        return 'CONNAISSANCE'
    elif comp_type == 'MACRO-SAVOIR-ETRE-PROFESSIONNEL':
        return 'SAVOIR_ETRE'
    elif comp_type == 'MACRO-SAVOIR-FAIRE':
        return 'SAVOIR_FAIRE'
    elif comp_type == 'COMPETENCE-DETAILLEE':
        macro_comp = comp.get('macroCompetence', {})
        sous_cat = macro_comp.get('sousCategorie', '')
        if sous_cat == 'TRANSVERSE':
            return 'SAVOIR_ETRE'
        else:
            return 'SAVOIR_FAIRE'
    else:
        return 'AUTRE'
```

```python
competences = get_competences()

if competences is None:
    print("Échec de récupération des compétences")
else:
    # Extraire tous les types uniques
    types_possibles = set()
    for comp in competences:
        types_possibles.add(comp.get('type', 'INCONNU'))

    print("Types possibles dans ROME 4.0:")
    for type_comp in sorted(types_possibles):
        print(f"  - {type_comp}")

    competences_detaillees = [c for c in competences if c.get('type') == 'COMPETENCE-DETAILLEE']
    print(f"\nAnalyse des {len(competences_detaillees)} COMPETENCE-DETAILLEE:")

    sous_categories = {}

    for comp in competences_detaillees:
        macro_comp = comp.get('macroCompetence', {})
        sous_cat = macro_comp.get('sousCategorie', 'INCONNU')

        if sous_cat not in sous_categories:
            sous_categories[sous_cat] = 0
        sous_categories[sous_cat] += 1

    print(f"\nSous-catégories:")
    for sous_cat, count in sous_categories.items():
        print(f"  - {sous_cat}: {count}")

with open('data/rome_competences.json', 'w') as f:
    json.dump(competences, f, indent=2)

print(f"\nDonnées sauvegardées:")
print(f"  - data/rome_competences.json (données brutes)")
```

```python
competences_mappees = []
for comp in competences:
    competences_mappees.append({
        'code': comp.get('code', ''),
        'libelle': comp.get('libelle', ''),
        'type': mapper_type_competence(comp)
    })

# Compter par type final
comptage_final = {}
for comp in competences_mappees:
    type_final = comp['type']
    if type_final not in comptage_final:
        comptage_final[type_final] = 0
    comptage_final[type_final] += 1

print(f"\nMapping final vers 3 catégories:")
for type_final, count in comptage_final.items():
    print(f"  - {type_final}: {count}")

with open('data/rome_competences_mappees.json', 'w') as f:
    json.dump(competences_mappees, f, indent=2)

print(f"\nDonnées sauvegardées:")
print(f"  - data/rome_competences_mappees.json (mapping propre)")
```
