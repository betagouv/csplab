```python
import os
import requests
import time
import matplotlib.pyplot as plt
import pandas as pd
import re
import json
```

```python
class PisteClient:
    def __init__(self):
        self.oauth_base_url = os.environ.get('PISTE_OAUTH_BASE_URL')
        self.ingres_base_url = os.environ.get('INGRES_BASE_URL')
        self.client_id = os.environ.get('INGRES_CLIENT_ID')
        self.client_secret = os.environ.get('INGRES_CLIENT_SECRET')
        self.access_token = None
        self.expires_at = 0

    def _get_token(self):
        response = requests.post(
            f'{self.oauth_base_url}/api/oauth/token',
            headers={
                'Accept': 'application/json',
            },
            data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'openid'
            }
        )
        data = response.json()
        self.access_token = data['access_token']
        self.expires_at = time.time() + data['expires_in']

    def _ensure_token(self):
        if not self.access_token or time.time() >= self.expires_at:
            self._get_token()

    def request(self, method, endpoint, **kwargs):
        self._ensure_token()
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {self.access_token}'
        kwargs['headers'] = headers
        return requests.request(method, f'{self.ingres_base_url}/{endpoint}', **kwargs)
```

```python
from IPython.display import JSON

client = PisteClient()

response = client.request('GET', 'RMFP_EMPL_REF', params={'enVigueur': 'true', 'full': 'true'})
body = response.json()
```

```python
with open('data/fixtures_ingres_rmfp_csp.json', 'w') as file:
    json.dump(body, file, indent=4)
JSON(body)
```

```python
len(body['items'])
```

```python
def parse_metier(item):
    """Parse un item RMFP pour extraire les informations de métier"""
    definitions = item.get('definitions', {})

    # Informations de base
    identifiant = item.get('identifiant')
    libelles = definitions.get('libelles', {})

    # Domaine fonctionnel et famille
    domaine_famille = definitions.get('domaineFonctionnel_Famille', {})

    return {
        'identifiant': identifiant,
        'libelle_court': libelles.get('libelleCourt'),
        'libelle_long': libelles.get('libelleLong'),
        'definition': definitions.get('definitionSynthetiqueDeLEr', {}).get('definition'),

        # Domaine fonctionnel
        'code_domaine': domaine_famille.get('codeDomaineFonctionnel'),
        'libelle_domaine': domaine_famille.get('libelleDomaineFonctionnel'),

        # Famille
        'code_famille': domaine_famille.get('codeFamille'),
        'libelle_famille': domaine_famille.get('libelleFamille'),

        # Fonction publique
        'fonction_publique': definitions.get('fonctionPublique', {}),

        # Emploi CSP
        'emploi_csp': definitions.get('emploiDeReferenceCSP', {})
    }

# Analyser tous les métiers
metiers_parsed = [parse_metier(item) for item in body['items']]

# Créer des DataFrames pour analyser
df_metiers = pd.DataFrame(metiers_parsed)

print("=== ANALYSE DES DOMAINES FONCTIONNELS ===")
domaines = df_metiers[['code_domaine', 'libelle_domaine']].drop_duplicates().sort_values('code_domaine')
print(f"Nombre de domaines uniques: {len(domaines)}")
print(domaines.head(10))

print("\n=== ANALYSE DES FAMILLES ===")
familles = df_metiers[['code_famille', 'libelle_famille']].drop_duplicates().sort_values('code_famille')
print(f"Nombre de familles uniques: {len(familles)}")
print(familles.head(10))

print("\n=== RELATION DOMAINE <-> FAMILLE ===")
relations = df_metiers[['code_domaine', 'libelle_domaine', 'code_famille', 'libelle_famille']].drop_duplicates()
print(f"Nombre de relations uniques: {len(relations)}")

# Vérifier si une famille peut appartenir à plusieurs domaines
familles_multi_domaines = relations.groupby(['code_famille', 'libelle_famille']).size()
familles_avec_plusieurs_domaines = familles_multi_domaines[familles_multi_domaines > 1]

if len(familles_avec_plusieurs_domaines) > 0:
    print("\n⚠️  FAMILLES APPARTENANT À PLUSIEURS DOMAINES:")
    print(familles_avec_plusieurs_domaines)
else:
    print("\n✅ Chaque famille appartient à un seul domaine")

# Vérifier la structure hiérarchique
print("\n=== STRUCTURE HIÉRARCHIQUE ===")
for domaine_code in domaines['code_domaine'].head(3):
    familles_du_domaine = relations[relations['code_domaine'] == domaine_code]
    print(f"\nDomaine {domaine_code}:")
    for _, famille in familles_du_domaine.iterrows():
        print(f"  └─ {famille['code_famille']}: {famille['libelle_famille']}")
```
