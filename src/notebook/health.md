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
import json
import requests
from dotenv import load_dotenv

BASE_URL = "https://csplab.beta.gouv.fr"

load_dotenv()
BOTYCHO_USERNAME = os.getenv("BOTYCHO_USERNAME")
BOTYCHO_PASSWORD = os.getenv("BOTYCHO_PASSWORD")

BOTYCHO_USERNAME is not None and BOTYCHO_PASSWORD is not None
```

```python
url = f"{BASE_URL}/api/token/"
payload = {"username": BOTYCHO_USERNAME, "password": BOTYCHO_PASSWORD}
headers = {"Content-Type": "application/json"}
resp = requests.post(url, headers=headers, json=payload)
resp.status_code == 200
```

```python
url = f"{BASE_URL}/ingestion/health/huey/"
headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
response = requests.get(url, headers=headers)
response.status_code == 200
```

```python
response.text
```
