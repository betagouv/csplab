```python
import re
from sqlalchemy import create_engine
import os

raw_url = os.getenv("WEB_DATABASE_URL", "postgresql+psycopg2://web:pass@localhost:5432/web")

# Normalise le schéma vers psycopg2 (psql://, postgres://, postgresql:// → postgresql+psycopg2://)
url = re.sub(r'^(?:postgresql|postgres|psql)(?:\+\w+)?://', 'postgresql+psycopg2://', raw_url)

engine = create_engine(url)
```

```python
import pandas as pd

df = pd.read_sql("""
    SELECT
        raw_data->>'reference'                                                   AS reference,
        raw_data->'salaryRange'->>'clientCode'                                   AS versant,
        raw_data->'contractType'->>'clientCode'                                  AS contract_type,
        raw_data->'customFields'->'offer'->'customCodeTable2'->>'clientCode'     AS contract_kind
    FROM ingestion_rawdocument
    WHERE document_type = 'OFFERS'
""", con=engine)

df = df.fillna("(vide)")

df.head()
```

```python
pd.crosstab(
    [df["versant"], df["contract_type"]],   # lignes : 2 dimensions
    df["contract_kind"],                    # colonnes
    margins=True,
    margins_name="Total"
)
```
