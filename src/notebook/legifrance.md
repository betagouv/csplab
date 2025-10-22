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
import pandas as pd
from pylegifrance import LegifranceClient
from pylegifrance.fonds.loda import Loda, TexteLoda
from pylegifrance.models.loda.search import SearchRequest
from itertools import takewhile, count

client = LegifranceClient()
loda = Loda(client)

def search_concours(page_num, year):
    search_request = SearchRequest(
        search=f"concours {year}",
        natures=["ARRETE", "DECISION"],
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

def get_all_pages(client: LegifranceClient, year: str, max_pages: int = 50):
    # retrieve all page until one is empty or we reach the 50 pages limit
    pages = takewhile(
        lambda results: len(results) > 0,
        (search_concours(page, year) for page in count(1) if page <= max_pages)
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
```

## Concours 2025

```{code-cell} ipython3
year_2025 = get_all_pages(client, "2025")
```

```{code-cell} ipython3
df = pd.DataFrame(year_2025)
df_clean = df.dropna(axis=1, how='all')
df_clean.head()
```

```{code-cell} ipython3
raw_content = get_raw_content("LEGITEXT000043462808_27-06-2025")
raw_content[:500]
```

```{code-cell} ipython3
from IPython.display import JSON
import json
law_details = get_law_details("LEGITEXT000043462808_27-06-2025")
JSON(law_details)
```

```{code-cell} ipython3
filename = "law_details.json"  # Nom de fichier en string
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(law_details, f, ensure_ascii=False, indent=2, default=str)
```

```{code-cell} ipython3
import re
from datetime import datetime

def extract_decret_numbers(raw_content):
    pattern = r'décret n°?\s*(\d{2,4}-\d+)'
    matches = re.findall(pattern, raw_content, re.IGNORECASE)
    return list(set(matches))
```

```{code-cell} ipython3
extract_decret_numbers(raw_content)
```

```{code-cell} ipython3
dict_str = str(law_details)
decrets = list(set(re.findall(r'Décret n°?\s*(\d{2,4}-\d+)', dict_str, re.IGNORECASE)))
decrets
```

# Recherche par Decret

+++

### Contexte

+++

Utile pour récupérer les statuts des corps par exemple, la recherche par nor ne fonctionne pas, l'id legifrance n'est pas toujours renseigné dans Ingres, mais la recherche par décret, an ajoutant un filtre sur le champ titre, aboutit

```{code-cell} ipython3
def search_by_decret(decret_number):
    search_request = SearchRequest(
        search=decret_number,
        page_size=20
    )
    results = loda.search(search_request)
    return results
all_decrets = sum([search_by_decret(decret) for decret in decrets], [])
unique_decrets = {decret.id: decret for decret in all_decrets}.keys()
```

```{code-cell} ipython3
unique_decrets
```

```{code-cell} ipython3
all_texts = [get_law_details(id)['title'] for id in unique_decrets]
```

```{code-cell} ipython3
all_texts
```

```{code-cell} ipython3
original_texts = [text_loda for text_loda in results
                 if text_loda.titre and corps_decret in text_loda.titre
                 and "modif" not in text_loda.titre.lower()]
original_texts
```

```{code-cell} ipython3
JSON(get_law_details("LEGITEXT000006061962_01-09-2024"))
```
