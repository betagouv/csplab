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
    # Récupère toutes les pages jusqu'à ce qu'une soit vide ou qu'on atteigne la limite
    pages = takewhile(
        lambda results: len(results) > 0,
        (search_concours(page, year) for page in count(1) if page <= max_pages)
    )

    return [result for page in pages for result in page]

def get_sample_results(client: LegifranceClient, year: str, sample_size: int = 5):
    # Récupère juste la première page
    first_page = search_concours(1, year)

    # Retourne seulement les N premiers résultats
    return first_page[:sample_size]
```

```{code-cell} ipython3
year_2025 = get_all_pages(client, "2025")
```

```{code-cell} ipython3
df = pd.DataFrame(year_2025)
df_clean = df.dropna(axis=1, how='all')
```

```{code-cell} ipython3
df_clean
```

```{code-cell} ipython3
def get_article(text_id: str):
    article = loda.fetch(text_id)
    if article and article._texte.consult_response:
        data = article._texte.consult_response.model_dump()
        return article.texte_brut
    return article
```

```{code-cell} ipython3
article = get_article("LEGITEXT000044338924_27-06-2025")
article
```

```{code-cell} ipython3

```
