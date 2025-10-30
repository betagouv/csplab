---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.3
kernelspec:
  name: csplab-concours
  display_name: CSPLab concours
  language: python
---

```{code-cell} ipython3
from dotenv import load_dotenv
from pylegifrance import ApiConfig
import os
import pandas as pd
from pylegifrance import LegifranceClient
from pylegifrance.fonds.loda import Loda, TexteLoda
from pylegifrance.models.loda.search import SearchRequest
from pylegifrance.models.generated.model import TypeChamp
from itertools import takewhile, count
from IPython.display import JSON
import json
import re
from datetime import datetime
```

```{code-cell} ipython3
load_dotenv()
try:
    config = ApiConfig.from_env()
    print(config.client_id)
    print("✅ Configuration chargée depuis les variables d'environnement")
    print(f"Client ID présent: {'✅' if config.client_id else '❌'}")
except ValueError as e:
    print(f"❌ Erreur: {e}")
```

# Recherche par mot-clé : concours et année

```{code-cell} ipython3
client = LegifranceClient()
loda = Loda(client)

def search_concours(page_num, year):
    search_request = SearchRequest(
        search=f"concours {year}",
        page_number=page_num,
        page_size=100
    )
    try:
        results = loda.search(search_request)
        processed_results = []
        for result in results:
            if result._texte.consult_response:
                result_dict = result._texte.consult_response.model_dump()
                processed_results.append(result_dict)
        return processed_results

    except Exception as e:
        print(f"❌ Erreur page {page_num}: {e}")
        return []

def search_by_decret(page_num, keyword):
    search_request = SearchRequest(
        search=keyword,
        page_number=page_num,
        page_size=100
    )
    try:
        return loda.search(search_request)
    except Exception as e:
        print(f"❌ Erreur page {page_num}: {e}")
        return []

def get_all_pages(client: LegifranceClient, keyword: str, search_func, max_pages: int = 50):
    pages = takewhile(
        lambda results: len(results) > 0,
        (search_func(page, keyword) for page in count(1) if page <= max_pages)
    )
    return [result for page in pages for result in page]

def get_raw_content(text_id: str):
    text = loda.fetch(text_id)
    raw_text = text.texte_brut
    if raw_text:
        return raw_text

def get_law_details(text_id: str):
    text = loda.fetch(text_id)
    if text and text._texte.consult_response:
       details = text._texte.consult_response.model_dump()
       return details

def extract_decret_numbers(raw_content):
    pattern = r'décret n°?\s*(\d{2,4}-\d+)'
    matches = re.findall(pattern, raw_content, re.IGNORECASE)
    return list(set(matches))
```

## Concours 2025

```{code-cell} ipython3
year_2025 = get_all_pages(client, "2025", search_concours)
```

```{code-cell} ipython3
df = pd.DataFrame(year_2025)
df_clean = df.dropna(axis=1, how='all')
df_clean.head()
```

```{code-cell} ipython3
raw_content = get_raw_content(df_clean['id'][0])
raw_content[:500]
```

```{code-cell} ipython3
law_details = get_law_details(df_clean['id'][0])
JSON(law_details)
```

```{code-cell} ipython3
extract_decret_numbers(str(law_details))
```

# Recherche par Decret

+++

### Contexte

+++

Utile pour récupérer les statuts des corps par exemple, la recherche par nor ne fonctionne pas, l'id legifrance n'est pas toujours renseigné dans Ingres, mais la recherche par décret, en ajoutant un filtre sur le champ titre, aboutit

```{code-cell} ipython3
df_corps = pd.read_csv('corps_decret_validate.csv', sep='\t', encoding='utf-8')
decrets = df_corps['selected_law_id'].unique()
clean_law_ids = [law_id for law_id in decrets if bool(re.match(r'^\d{2,4}-\d+$', str(law_id)))]
len(decrets), len(clean_law_ids)
```

```{code-cell} ipython3
clean_law_ids[:10]
```

```{code-cell} ipython3
all_texts = get_all_pages(client, '90-973', search_by_decret)
all_texts
```

```{code-cell} ipython3
JSON(get_law_details(all_texts[0].id))
```
