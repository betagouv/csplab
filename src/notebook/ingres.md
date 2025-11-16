```python
import os
import requests
import time
import matplotlib.pyplot as plt
import pandas as pd
import re
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
        print(os.environ.get('PISTE_OAUTH_BASE_URL'))
        print(os.environ.get('INGRES_BASE_URL'))
        print(os.environ.get('INGRES_CLIENT_ID'))
        print(os.environ.get('INGRES_CLIENT_SECRET'))

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

response = client.request('GET', 'CORPS', params={'enVigueur': 'true', 'full': 'true'})
body = response.json()
```

```python
JSON(body)
```

```python
len(body['items'])
```

```python
def corps_parser(item):
    corps_libelle = item['corpsOuPseudoCorps']['libelles']['libelleLong']

    sub_category = None
    if item['corpsOuPseudoCorps']['sousCategorie']:
        sub_category = item['corpsOuPseudoCorps']['sousCategorie'][0]['libelleSousCategorie']

    category = None
    if sub_category:
        category = sub_category
    elif item['corpsOuPseudoCorps']['caracteristiques']['categorie']['libelleCategorie'][-1] != "e":
        category = item['corpsOuPseudoCorps']['caracteristiques']['categorie']['libelleCategorie'][-1]


    branch = None
    if item['corpsOuPseudoCorps']['caracteristiques']['filiere']:
        branch = item['corpsOuPseudoCorps']['caracteristiques']['filiere']['libelleFiliere']

    diploma = None
    if item['corpsOuPseudoCorps']['caracteristiques']['niveauDiplome']:
        diploma = item['corpsOuPseudoCorps']['caracteristiques']['niveauDiplome']['libelleNiveauDiplome']

    access_mod = []
    if item['corpsOuPseudoCorps']['dureeDeStageParModeAccesAuCorps']:
        access_mod = [mod['modeAccesCorps']['libelleModeAccesCorps'] for mod in item['corpsOuPseudoCorps']['dureeDeStageParModeAccesAuCorps']]

    ministry = None
    if item['corpsOuPseudoCorps']['ministereEtInstitutionDeLaRepublique']:
        ministry = item['corpsOuPseudoCorps']['ministereEtInstitutionDeLaRepublique'][0]['libelleMinistere']

    population = None
    if item['corpsOuPseudoCorps']['caracteristiques']['population']:
        population = item['corpsOuPseudoCorps']['caracteristiques']['population']['libellePopulation']

    law_ids = None
    if item['definitionsHistoriques']['textesAssocies']:
        law_ids = [text['numeroTexte'] for text in item['definitionsHistoriques']['textesAssocies']]

    law_desc = None
    if item['definitionsHistoriques']['textesAssocies']:
        law_desc = [text['descriptif'] for text in item['definitionsHistoriques']['textesAssocies']]

    law_nature = None
    if item['definitionsHistoriques']['textesAssocies']:
        law_nature = [text['nature']['libelleNature'] for text in item['definitionsHistoriques']['textesAssocies'] if text['nature']]

    return {
        'id': item['identifiant'],
        'category': category,
        'short_label': item['corpsOuPseudoCorps']['libelles']['libelleCourt'],
        'long_label': corps_libelle,
        'access_mod': access_mod,
        'branch': branch,
        'diploma': diploma,
        'ministry': ministry,
        'fp_type': item['corpsOuPseudoCorps']['caracteristiques']['natureFonctionPublique']['libelleNatureFoncPub'],
        'population': population,
        'law_ids': law_ids,
        'law_desc': law_desc,
        'law_nature': law_nature
    }
```

```python
corps = [corps_parser(item) for item in body['items']]
df = pd.DataFrame(corps)

only_fpe = df['fp_type'] == 'FPE'
no_minarm = df['ministry'] != 'MINARM'
fonctionnaire = df['population'] == "Fonctionnaire"

conditions = {
    'only_fpe':only_fpe,
    'no_minarm':no_minarm,
    'fonctionnaire': fonctionnaire
}

for condition_label, condition in conditions.items():
    print(condition_label, len(df[condition]))

df['branch'].isnull().sum()
df.drop(['fp_type', 'branch'], axis=1, inplace=True)

df = df[no_minarm & fonctionnaire]

df_expanded = df.explode(['law_ids', 'law_desc', 'law_nature']).rename(columns={
    'law_ids': 'law_id',
    'law_desc': 'law_desc',
    'law_nature': 'law_nature'
})
df_expanded = df_expanded.dropna(subset=['law_id'])

df_expanded
```

```python
frequencies = df_expanded['law_id'].value_counts()
# Créer le diagramme en bâtons
plt.figure(figsize=(12, 6))
frequencies.plot(kind='bar')
plt.title('Fréquences des Law IDs')
plt.xlabel('Law ID')
plt.ylabel('Nombre d\'occurrences')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

```python
law_freq = pd.DataFrame(frequencies).reset_index()
law_freq.columns = ['law_id', 'count']
df_rule = df_expanded.merge(law_freq, on='law_id', how='left')

# Convert DataFrame to list of dicts
data_dicts = df_rule.to_dict('records')

# Group by corps_id
corps_groups = {}
for row in data_dicts:
    corps_id = row['id']
    if corps_id not in corps_groups:
        corps_groups[corps_id] = []
    corps_groups[corps_id].append(row)
```

```python
def has_valid_decree_format(law_id):
    """Check if law_id has valid decree format (YYYY-NNNN or YY-NNNN)"""
    if not law_id:
        return False
    pattern = r'^\d{2,4}-\d+$'
    return bool(re.match(pattern, str(law_id)))


def select_best_law(laws_list):
    """Select best law from list of law dictionaries - prioritize valid decree format"""
    # rule 1: filter out too generic laws (referenced in more than 20 bodies)
    candidates = [law for law in laws_list if law['count'] <= 20]

    if not candidates:
        return None

    # rule 2: valid decree format (regardless of nature)
    valid_decree_laws = [law for law in candidates if has_valid_decree_format(law['law_id'])]

    if not valid_decree_laws:
        return None

    # rule 3: prefer origin texts, the most specific one (i.e. the least frequent one)
    origin_valid = [law for law in valid_decree_laws if law['law_nature'] == "Texte d'origine"]
    if origin_valid:
        return min(origin_valid, key=lambda x: x['count'])

    # rule 4: otherwise, modificative texts, the most specific one (i.e. the least frequent one)
    modif_valid = [law for law in valid_decree_laws if law['law_nature'] == "Texte modificatif"]
    if modif_valid:
        return min(modif_valid, key=lambda x: x['count'])

    # rule 5: fallback on least frequent
    return min(candidates, key=lambda x: x['count'])
```

```python
def test_corps_selection():
    # Test corps 563
    selected_563 = select_best_law(corps_groups['00563'])
    print(f"Corps 563 - Selected: {selected_563['law_id']} ({selected_563['law_nature']})")
    print(f"Corps 563 - Valid format: {has_valid_decree_format(selected_563['law_id'])}")

    # Test corps 263
    selected_263 = select_best_law(corps_groups['00263'])
    print(f"Corps 263 - Selected: {selected_263['law_id']} ({selected_263['law_nature']})")
    print(f"Corps 263 - Valid format: {has_valid_decree_format(selected_263['law_id'])}")

    # Vérification que les deux ont un format valide
    assert has_valid_decree_format(selected_563['law_id']), "Corps 563 should have valid decree format"
    assert has_valid_decree_format(selected_263['law_id']), "Corps 263 should have valid decree format"
    print("✅ Tests passed: Both corps have valid decree format")

# Exécuter le test
test_corps_selection()
```

```python
# Process each corps
results = []
filtered_out = 0
for corps_id, laws_list in corps_groups.items():
    base_info = laws_list[0]  # First row for base info

    # Get all laws info
    all_law_ids = [law['law_id'] for law in laws_list]
    all_law_desc = [law['law_desc'] for law in laws_list]
    all_law_nature = [law['law_nature'] for law in laws_list]

    # Select best law
    selected_law = select_best_law(laws_list)

    if selected_law:
        result = {
            'id': corps_id,
            'category': base_info['category'],
            'short_label': base_info['short_label'],
            'long_label': base_info['long_label'],
            'selected_law_id': selected_law['law_id'],
            'selected_law_desc': selected_law['law_desc'],
            'selected_law_nature': selected_law['law_nature'],
            'selected_count': selected_law['count'],
            'all_law_ids': all_law_ids,
            'all_law_desc': all_law_desc,
            'all_law_nature': all_law_nature
        }
        results.append(result)
    else:
        filtered_out += 1

print(f"Corps conservés: {len(results)}")
print(f"Corps filtrés: {filtered_out}")
print(f"Total: {len(results) + filtered_out}")

df_clean = pd.DataFrame(results)
df_clean
```

```python
import json
json_list = df_clean.to_dict('records')
filename = "corps_index.json"
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(json_list, f, ensure_ascii=False, indent=2, default=str)
```

```python
df_clean.to_csv('corps_decret_validate.csv', sep='\t', index=False, encoding='utf-8')
```

```python

```
