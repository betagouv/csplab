```python
from dotenv import load_dotenv
import os
```

```python
load_dotenv()
oauth_base_url = os.getenv('PISTE_OAUTH_BASE_URL')
ingres_base_url = os.getenv('INGRES_BASE_URL')
client_id = os.getenv('INGRES_CLIENT_ID')
client_secret = os.getenv('INGRES_CLIENT_SECRET')
print(oauth_base_url)
```

```python
import requests

response = requests.post(
    f'{oauth_base_url}/api/oauth/token',
    headers={
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Connection': 'Keep-Alive'
    },
    data={
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'openid'
    }
)
```

```python
body = response.json()
access_token = body['access_token']
access_token
```

```python
body
```

```python
import time

class PisteClient:
    def __init__(self):
        load_dotenv()
        self.oauth_base_url = os.getenv('PISTE_OAUTH_BASE_URL')
        self.ingres_base_url = os.getenv('INGRES_BASE_URL')
        self.client_id = os.getenv('INGRES_CLIENT_ID')
        self.client_secret = os.getenv('INGRES_CLIENT_SECRET')
        self.access_token = None
        self.expires_at = 0

    def _get_token(self):
        response = requests.post(
            f'{self.oauth_base_url}/api/oauth/token',
            headers={
                'Accept-Encoding': 'gzip, deflate',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
                'Connection': 'Keep-Alive'
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
import json

client = PisteClient()

response = client.request('GET', 'CORPS', params={'enVigueur': 'true', 'full': 'true'})
body = response.json()
JSON(body)
```

```python
len(body['items'])
```

```python
def corps_parser(item):
    sub_category = None
    if item['corpsOuPseudoCorps']['sousCategorie']:
        sub_category = item['corpsOuPseudoCorps']['sousCategorie'][0]['libelleSousCategorie']

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

    origin_law_ids = None
    if item['definitionsHistoriques']['textesAssocies']:
        origin_law_ids = [text['numeroTexte'] for text in item['definitionsHistoriques']['textesAssocies'] if text['nature']['libelleNature'] == "Texte d'origine"]

    origin_law_desc = None
    if item['definitionsHistoriques']['textesAssocies']:
        origin_law_desc = [text['descriptif'] for text in item['definitionsHistoriques']['textesAssocies'] if text['nature']['libelleNature'] == "Texte d'origine"]

    return {
        'id': item['identifiant'],
        'category': sub_category or item['corpsOuPseudoCorps']['caracteristiques']['categorie']['libelleCategorie'][-1],
    	'short_label': item['corpsOuPseudoCorps']['libelles']['libelleCourt'],
        'long_label': item['corpsOuPseudoCorps']['libelles']['libelleLong'],
        'access_mod': access_mod,
    	'branch': branch,
    	'diploma': diploma,
    	'ministry': ministry,
        'fp_type': item['corpsOuPseudoCorps']['caracteristiques']['natureFonctionPublique']['libelleNatureFoncPub'],
        'origin_law_ids': origin_law_ids,
        'origin_law_desc': origin_law_desc
    }
```

```python
corps = [corps_parser(item) for item in body['items']]
```

```python
import pandas as pd
df = pd.DataFrame(corps)

only_fpe = df['fp_type'] == 'FPE'
no_minarm = df['ministry'] != 'MINARM'

conditions = {
    'only_fpe':only_fpe,
    'no_minarm':no_minarm,
}

for condition_label, condition in conditions.items():
    print(condition_label, len(df[condition]))

df['branch'].isnull().sum()
```

```python
df.drop(['fp_type', 'branch'], axis=1, inplace=True)
df_clean = df[many_original_text]
df_clean
```
